So, this looks a lot like the password game - no way I'll do this lmao.

Let's save the webpage and see if we can reverse it.

From the obfuscated JavaScript code, at the bottom of the rules we find something interesting.. hash checksums!
And from the looks of it there's a checksum for every 2nd character in the flag, nice!

So, using this, together with the other rules, should result in a pretty fast flag solver - we'll implement it in Python.

And after a bit of coding, boom flag: got!

hkcert23{h0p3_y0u_u53d_th3_s0urc3m4p}