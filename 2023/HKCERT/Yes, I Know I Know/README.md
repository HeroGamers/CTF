In the chal.pcapng file we find some DNS queries to a locally hosted service run at 192.168.135.135 (igotoschoolbybus.online).

Two powershell scrips are requested, which we save.

We find this: https://github.com/Arno0x/DNSExfiltrator

We can then download the python server script, insert the queries from Wireshark, modify it a lil bit to work for Python 3 and badabing badaboom, we get the flag!

hkcert23{v3ry_5n34ky_w17h_dn53xf1l7r470r_5345623}