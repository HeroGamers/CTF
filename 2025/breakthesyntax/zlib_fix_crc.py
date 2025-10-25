import zlib
import struct
import sys

n_remove = 4

def calculate_crc(chunk_type, chunk_data):
    """Calculate the CRC for a PNG chunk."""
    return zlib.crc32(chunk_type + chunk_data) & 0xffffffff

def repair_png_chunk_length(filename, output_filename=None):
    """
    Find and repair a PNG chunk that's n_remove bytes too long by removing those bytes
    and checking the CRC.
    
    Args:
        filename: Input PNG file
        output_filename: Output fixed PNG file (if None, will add '_fixed' to the original name)
    """
    if output_filename is None:
        output_filename = filename.rsplit('.', 1)[0] + '_fixed.png'
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Check PNG signature
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        print("Not a valid PNG file")
        return False
    
    pos = 8  # Start after the PNG signature
    chunk_number = 0
    fixed = False
    
    # Process each chunk
    while pos < len(data):
        # Read chunk length and type
        chunk_length = struct.unpack('>I', data[pos:pos+4])[0]
        chunk_type = data[pos+4:pos+8]
        chunk_data = data[pos+8:pos+8+chunk_length]
        chunk_crc = struct.unpack('>I', data[pos+8+chunk_length:pos+8+chunk_length+4])[0]
        
        # Calculate actual CRC
        actual_crc = calculate_crc(chunk_type, chunk_data)
        
        chunk_name = chunk_type.decode('ascii', errors='replace')
        print(f"Chunk #{chunk_number}: {chunk_name}, Length: {chunk_length}, CRC: {chunk_crc:08x}, Calculated CRC: {actual_crc:08x}")
        
        # Check if CRC matches
        if actual_crc != chunk_crc:
            print(f"CRC mismatch in {chunk_name} chunk! Attempting to fix by removing n_remove bytes...")
            
            # Try removing n_remove consecutive bytes at different positions
            for i in range(chunk_length - n_remove + 1):
                # Create a new chunk data with n_remove bytes removed at position i
                new_chunk_data = chunk_data[:i] + chunk_data[i+n_remove:]
                new_crc = calculate_crc(chunk_type, new_chunk_data)
                
                if new_crc == chunk_crc:
                    print(f"Found fix! Removing n_remove bytes starting at position {i}")
                    
                    # Create the fixed PNG data
                    # Update chunk length (reduced by n_remove)
                    new_chunk_length = chunk_length - n_remove
                    new_length_bytes = struct.pack('>I', new_chunk_length)
                    
                    fixed_data = (
                        data[:pos] +                            # Everything before this chunk
                        new_length_bytes +                      # New chunk length
                        chunk_type +                            # Chunk type
                        new_chunk_data +                        # Fixed chunk data
                        data[pos+8+chunk_length:]               # Everything after this chunk
                    )
                    
                    with open(output_filename, 'wb') as f:
                        f.write(fixed_data)
                    
                    print(f"Fixed PNG saved to {output_filename}")
                    print(f"Removed bytes (hex): {chunk_data[i:i+n_remove].hex()}")
                    return True
            
            print(f"Could not find a fix by removing n_remove bytes from chunk {chunk_name}.")
        
        # Move to the next chunk
        pos += 8 + chunk_length + 4
        chunk_number += 1
    
    print("No CRC errors found or fixed.")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_png> [output_png]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    repair_png_chunk_length(input_file, output_file)
