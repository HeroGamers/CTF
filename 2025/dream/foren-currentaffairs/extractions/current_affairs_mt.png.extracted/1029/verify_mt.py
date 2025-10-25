#!/usr/bin/env python3
import argparse
import json
import hashlib
import concurrent.futures
import sys
import os
import time
from typing import Optional, List, Iterator

def worker_chunk(chunk: List[str], salt: bytes, iters: int, dklen: int, target: bytes) -> Optional[str]:
    """Process a chunk of words, returning the matching password if found."""
    for word in chunk:
        try:
            # Encode the word and compute PBKDF2
            dk = hashlib.pbkdf2_hmac("sha256", word.encode("utf-8"), salt, iters, dklen=dklen)
            if dk == target:
                return word
        except UnicodeEncodeError:
            # Skip words that can't be encoded
            continue
    return None

def chunks(lst: List[str], n: int) -> Iterator[List[str]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def load_wordlist(filepath: str) -> List[str]:
    """Load and clean wordlist from file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            words = []
            for line in f:
                word = line.strip()
                if word and not word.startswith('#'):  # Skip empty lines and comments
                    words.append(word)
        return words
    except FileNotFoundError:
        print(f"[-] Error: Wordlist file '{filepath}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error reading wordlist: {e}", file=sys.stderr)
        sys.exit(1)

def load_hash_info(filepath: str) -> dict:
    """Load hash information from JSON file."""
    try:
        with open(filepath, "r") as f:
            info = json.load(f)
        
        # Validate required fields
        required_fields = ["salt_hex", "hash_hex", "iterations", "dklen"]
        for field in required_fields:
            if field not in info:
                print(f"[-] Error: Missing required field '{field}' in hash JSON", file=sys.stderr)
                sys.exit(1)
        
        return info
    except FileNotFoundError:
        print(f"[-] Error: Hash file '{filepath}' not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[-] Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error reading hash file: {e}", file=sys.stderr)
        sys.exit(1)

def calculate_optimal_chunk_size(total_words: int, num_threads: int) -> int:
    """Calculate optimal chunk size based on wordlist size and thread count."""
    # Aim for roughly 4-8 chunks per thread to balance load distribution and overhead
    target_chunks_per_thread = 6
    optimal_chunks = num_threads * target_chunks_per_thread
    chunk_size = max(50, min(1000, total_words // optimal_chunks))
    return chunk_size

def main():
    ap = argparse.ArgumentParser(description="PBKDF2 password cracker with multiprocessing")
    ap.add_argument("hash_json", help="JSON file containing hash parameters")
    ap.add_argument("wordlist", help="Wordlist file to test")
    ap.add_argument("-t", "--threads", type=int, default=os.cpu_count() or 2, 
                   help=f"Number of worker processes (default: {os.cpu_count() or 2})")
    ap.add_argument("--chunk", type=int, help="Words per task (auto-calculated if not specified)")
    ap.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = ap.parse_args()

    # Load data
    if args.verbose:
        print(f"[*] Loading hash information from {args.hash_json}", file=sys.stderr)
    info = load_hash_info(args.hash_json)
    
    if args.verbose:
        print(f"[*] Loading wordlist from {args.wordlist}", file=sys.stderr)
    words = load_wordlist(args.wordlist)
    
    # Parse hash parameters
    try:
        salt = bytes.fromhex(info["salt_hex"])
        target = bytes.fromhex(info["hash_hex"])
        iters = int(info["iterations"])
        dklen = int(info["dklen"])
    except ValueError as e:
        print(f"[-] Error parsing hash parameters: {e}", file=sys.stderr)
        sys.exit(1)

    # Calculate chunk size
    if args.chunk:
        chunk_size = max(1, args.chunk)
    else:
        chunk_size = calculate_optimal_chunk_size(len(words), args.threads)
    
    print(f"[*] Loaded {len(words)} words", file=sys.stderr)
    print(f"[*] Using {args.threads} threads with chunk size {chunk_size}", file=sys.stderr)
    print(f"[*] Target: {info['iterations']} iterations, salt: {info['salt_hex'][:16]}...", file=sys.stderr)
    
    start_time = time.time()
    found = None
    words_processed = 0

    try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.threads) as executor:
            # Submit all chunks
            future_to_chunk = {
                executor.submit(worker_chunk, chunk, salt, iters, dklen, target): len(chunk)
                for chunk in chunks(words, chunk_size)
            }
            
            total_chunks = len(future_to_chunk)
            completed_chunks = 0
            
            print(f"[*] Processing {total_chunks} chunks...", file=sys.stderr)
            
            for future in concurrent.futures.as_completed(future_to_chunk):
                completed_chunks += 1
                chunk_size_actual = future_to_chunk[future]
                words_processed += chunk_size_actual
                
                try:
                    result = future.result()
                    if result:
                        found = result
                        # Cancel remaining futures
                        for f in future_to_chunk:
                            f.cancel()
                        break
                        
                    # Progress reporting (every 10% or every 100 chunks, whichever is less frequent)
                    if completed_chunks % max(1, min(100, total_chunks // 10)) == 0:
                        elapsed = time.time() - start_time
                        rate = words_processed / elapsed if elapsed > 0 else 0
                        progress = (completed_chunks / total_chunks) * 100
                        print(f"[*] Progress: {progress:.1f}% ({words_processed}/{len(words)} words, {rate:.0f} words/sec)", 
                              file=sys.stderr)
                        
                except Exception as e:
                    print(f"[-] Worker error: {e}", file=sys.stderr)
                    continue

    except KeyboardInterrupt:
        print("\n[-] Interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"[-] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

    elapsed_time = time.time() - start_time
    
    if found:
        print(f"\n[+] Password found: {found}")
        print(f"[+] Flag: DREAM{{{found}}}")
        print(f"[+] Search completed in {elapsed_time:.2f} seconds ({words_processed} words processed)", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"\n[-] Password not found in wordlist")
        print(f"[-] Searched {words_processed} words in {elapsed_time:.2f} seconds", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
