Load the images into Autopsy.

Find the user has downloaded a MobaXterm and KeePass.

Get the KeePass database by searching for .kdbx files in Autopsy (since it's version 2.x).
Get the KeePass config from appdata.

Try opening the KeePass database into KeePass - we need the master password.



Find the MobaXterm backup zip file, and get the .ini files.

Find the following lines:
[Credentials]
DDC=FLAG:_@8MOT3P3M67ot8NKNWGW7V0soyAT5xKDVxaUpB5D0L9sKoFx8OaBQMcTrv5

Find out online, how MobaXterm encrypts the credentials. There are (old) tools for various versions, so let's try them all. Some only work on Windows :/

https://github.com/xillwillx/MobaXterm-Decryptor

which is a fork of
https://github.com/HyperSine/how-does-MobaXterm-encrypt-password

Tried putting the session ID and host name + user into those, but it couldn't decrypt it...

(this one is a exe, but seems to work directly on the ini files!)
https://github.com/h0ny/MobaXtermDecryptor


Also found this one
https://xmcyber.com/blog/extracting-encrypted-credentials-from-common-tools-2/

Which links to https://github.com/XMCyber/XMCredentialsDecryptor

But that wants to read from registry, and took a bit too long to modify. Already tried 2-3 other tools, and CTF was about to end.