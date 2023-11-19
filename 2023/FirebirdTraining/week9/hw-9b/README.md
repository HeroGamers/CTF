For this challenge, I decided that I was too lazy to keep opening z7ip/winrar and changing the metadata, when I could just write a little script to do it for me?
Easy? please say yes!

First we want to know what our index file looks like, so our first goal is the following payload: `php://filter/convert.base64-encode/resource=index.php`.
We execute it and save the file. Nice, now we know that the admin page is indeed located at "admin.php", which we can also get.

Oh, so the way it checks for local host is the following: `$_SERVER['REMOTE_ADDR'] !== "127.0.0.1"`. Sadly, there seems to be [no way to bypass this](https://security.stackexchange.com/questions/249577/changing-serverremote-addr-remotely).

So, time to find a SSRF vuln such that we can have the server itself send a request to admin.php?

It seems that if we use the payload `php://filter/convert.base64-encode/resource=http://localhost/admin.php`, then we successfully get a SSRF! However, we need to send a POST request.. hmm..
Just out of curiosity, I tried the following `php://filter/convert.base64-encode/resource=http://localhost/admin.php?cmd=ls`, and low and behold, we get the files in the directory!

Nice, now to get the flag!

`php://filter/convert.base64-encode/resource=http://localhost/admin.php?cmd=ls%20../../../` -> `flag_ab8393a93a942f257c4bf6ae1cc63cc0`

Use the cat, and boom, flag: got!

`flag{1oC4lh05t_w45_h4ck3d_8y_y0u!}`
