HW 4-B Simple Encryption

# Variables

- key is the encryption key
- flag is the flag, and starts with "flag{" and ends with "}"
- k is the key represented as long
- m is the flag represented as long
- n is prime
- n is smaller than m
- key and flag has same length


# Encryption

c1 is calculated by modulo arithmetic: c1 = (k * m) % n
c2 is calculated by XOR'ing the flag with the key: c2 = xor(key, flag)


We are provided with n:
n = 150095186069281777851468726257751810997446691788728681013850021750670480757667073571298768531705071802820728411143863036993470518226749117889851508979626068982736226357060650073869307154521010066655609905126167748092779979732912821644834005606143609309269768565568485061354218686729973438920060109916387047693

And c1 and c2 in base64 encoding:
c1 = Lrh/EMfrRXqShQQqw+Zd/w6Nn2MwaWT5s0Xvb6AAq+NE4FxIvvPSuzLJbv9VwcJv0F1LlOfnfvc3j/eFM5BWpTujw6dQ8ZtjV6dOqqnLPC1lKdDZEmt5XaINbKe4CIIT37V1qtR2jqy7K1xjCUJJyGkrgFI9vXWyfrQAHo2JSt4=
c2 = ////////+/33/////////////////v////////////////9///////f/////////////3//f////////////////


# Cryptanalysis

We know that the flag starts with "flag{" and ends with "}", we can use this to give us the start and the end of the unknown key:

key[:5] = xor(c2[:5], b"flag{") = b"\x99\x93\x9e\x98\x84"
key[-1] = xor(c2[-1], b"}") = b"\x82"

c2 looks kinda fun, and sorta like the key was generated like this?

key = flag ^ 11111 (and some random 0's?)
encryptkey = key ^ flag = flag ^ 11111 ^ flag = 11111
encryptkey ^ key = 11111 ^ key = 11111 ^ flag ^ 11111 = flag

But that seems like your only way of finding the key is still by "bruteforcing" the flag.

It doesn't seem that you can efficiently bruteforce the flag by trying all alphanumeric combinations, since that would take ages.
So maybe a wordlist or something like that would help..? But that doesn't seem intended.

I tried to find a way to get the key from c1, but I couldn't find anything.
c1, if anything, seems like a good way to check whether you have found the correct flag, and can be computed pretty efficiently using CRT.

So from here, welp...? Idk what to do lol