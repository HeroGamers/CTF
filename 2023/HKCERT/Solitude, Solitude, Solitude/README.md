We have a Shamir's Secret Sharing, but we only have one share.

The following coefficient evaluation let's say coeffs = [11, 22, 33], x=3 and p=100000:

    ```
y = (y * x + coeff) % p

y = (0 * 3 + 33) % 100000 = 33
y = (33 * 3 + 22) % 100000 = 121
y = (121 * 3 + 11) % 100000 = 364
    ```
