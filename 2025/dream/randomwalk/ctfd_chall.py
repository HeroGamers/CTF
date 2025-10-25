from Crypto.Util.number import bytes_to_long
import os

FLAG = os.getenv('FLAG')

mults = 4

numbers = [bytes_to_long(os.urandom(3)) for i in range(mults)]

ns = []

def hash24(x):
    x = x & 0xFFFFFF
    x ^= x >> 12
    for num in numbers:
        x = (x * num) & 0xFFFFFF
        x ^= x >> 9
    return x

hashlookup = {}
rhashlookup = {}

print("creating hashtable please wait a moment", flush=True)

for i in range(2**24):
    h = hash24(i)
    hashlookup[i] = h
    rhashlookup[h] = i

print("done!")

def hash(x):
    return hashlookup[x]

def inversehash(h):
    return rhashlookup[h]

def getinverse():
    try:
        h = int(input("hash: "))
        assert ((h < 2**24) & (h > 26))
    except:
        print("invalid hash")
        return 0
    try:
        print(inversehash(h))
        return 1
    except:
        print("hash does not exist")
        return 0

def walk():
    try:
        n, m = map(int, input("n, m: ").split())
        assert ((n > 0) & (n < 2**24) & (m > 0) & (m < 2**24))
    except:
        print("invalid n and m")
        return 0
    if(n in ns):
        print("n already used")
        return 0
    ns.append(n)
    n = hash(n)
    for _ in range(n):
        m = hash(m)
    
    print(f'hashes: {n} {m}')

    return (n-m)//abs(n-m)
    

def main():
    randomwalks = 50
    inverses = 25
    position = 0
    while randomwalks > 0:
        command = input('[cmd] ')
        try:
            if command == 'inverse':
                if(inverses <= 0):
                    print("out of inverses")
                i = getinverse()
                inverses-=i
            elif command == 'walk':
                direction = walk()
                position += direction
                randomwalks-=1
                if(position == 50):
                    raise Exception("walk doesn't seem random :(")
        except:
            print(FLAG)
            break

if __name__ == '__main__':
    main()
