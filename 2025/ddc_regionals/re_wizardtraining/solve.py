import os

def magic(password):
    """
    public static String magic(String input) {
        long j = 1337;
        int k = 57 - 30 + 3 + 1;  
        int l = 222/6;  
        
        for (int i = 0; i < input.length(); i++) {
            j *= (input.charAt(i) + k) * l;
            j %= 1_000_000_007;
        }
        
        j = ((j << 16) | (j >> 48)) & 0xFFFFFFFFFFFFL;
        return Long.toHexString(j);
    }
    """
    j = 1337
    k = 57 - 30 + 3 + 1
    l = 222 // 6

    for char in password:
        j *= (ord(char) + k) * l
        j %= 1_000_000_007

    j = ((j << 16) | (j >> 48)) & 0xFFFFFFFFFFFF
    return hex(j)[2:]


def bruteforce_magic(ID, wordlist):
    for word in wordlist:
        if magic(word) == ID:
            return word
    return None


def main():
    with open("wordlist.txt") as f:
        wordlist = f.read().splitlines()
    
    # ID
    ID = "336db7f20000"

    # Find the password
    password = bruteforce_magic(ID, wordlist)
    if password:
        print(f"Password found: {password}")
    else:
        print("Password not found.")
    


if __name__ == "__main__":
    # Change directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    main()