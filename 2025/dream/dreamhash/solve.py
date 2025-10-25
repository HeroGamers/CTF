
import hashlib

def hash(data):
    """first segment + reverse(sha256(md5(sha512(IPv4))))"""
    # Calculate the SHA-512 hash of the input data
    sha512_hash = hashlib.sha512(data.encode()).digest()
    
    # Calculate the MD5 hash of the SHA-512 hash
    md5_hash = hashlib.md5(sha512_hash).digest()
    
    # Calculate the SHA-256 hash of the MD5 hash
    sha256_hash = hashlib.sha256(md5_hash).digest()
    
    # Reverse the SHA-256 hash
    reversed_sha256 = sha256_hash[::-1]
    
    # Convert to hexadecimal string and return
    return reversed_sha256.hex()

def solve():
    """
    <p>For example, <code>185.213.154.248</code>, becomes:</p>
    <code>18541e8bb8f31005d79fee5961c6298e76f77126751756a26df4ccf986ee51f8b62</code>
    <p>And <code>193.40.225.195</code> becomes:</p>
    <code>19327b948866cb3002ce04ca7a7ded3e2a07c71e002bb956591a6df6f73197c42cd</code>
    <p>The attacker's hash is:</p>
    <code>51b6f9a5bb5907bf876f4ca65ce3523ca56192194a3f759c0971f300ae24c4561b</code>
    """
    # Call the hash function with the provided data
    hash1 = hash("185.213.154.248")
    assert hash1 == "18541e8bb8f31005d79fee5961c6298e76f77126751756a26df4ccf986ee51f8b62"
    hash2 = hash("193.40.225.195")
    assert hash2 == "19327b948866cb3002ce04ca7a7ded3e2a07c71e002bb956591a6df6f73197c42cd"

    # Brute-force the hash to find the original IP address
    for i in range(256):
        for j in range(256):
            for k in range(256):
                for l in range(256):
                    ip = f"{i}.{j}.{k}.{l}"
                    if hash(ip) == "51b6f9a5bb5907bf876f4ca65ce3523ca56192194a3f759c0971f300ae24c4561b":
                        print(f"Found IP: {ip}")
                        return ip
    print("No matching IP found.")
    return None
