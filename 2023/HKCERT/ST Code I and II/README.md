# Part I

When we access /flag1 we get a QR code with rx=0 or rx=1 for each rect element. This is a binary string encoding.

For this I whipped up a Python script where I simply looped through and took out the binary and converted to ascii.

hkcert23{ST_ST&s4_STegan0graphy--STeg0}

# Part II

For this part, we first need to create a QR-code with flag1 inside (which the server has to accept) to get started.
After this, the server will provide us with some example data to encode into QR-codes and also ST-data which we need to encode in binary like in Part 1.

I originally tried to do it in Python, which was a mistake since the JavaScript server's Python libraries were kinda angry at how to handle files and such.

So I ended up rewriting it in JavaScript by stealing the server source code and writing new binary encryption functions.

We run into a little author fun at QR code number 11 when the length of the ST string is longer than the QR code, but nothing we can't fix with more rect elements.

hkcert23{ST_ST&s4_Speeeeeeed_&_Tricks--cksckscks}