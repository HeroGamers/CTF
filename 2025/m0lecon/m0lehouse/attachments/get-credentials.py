import sys
import hashlib

# Sorry for this

teams=['Kalmarunionen', 'IcySea', 'organizers', 'idek', 'Zer0Tolerance', 'thehackerscrew', 'PIG SEK@1', 'The Flat Network Society', '0ops', 'Tower of Hanoi']

if len(sys.argv)!=3:
    print("Usage: python3 get-credentials.py <team name> <your platform password>")
    exit(-1)

team = sys.argv[1]
password = sys.argv[2]

if team not in teams:
    print("You sure you are competing in this competition?")
    exit(-1)

ssh_port = 2220+teams.index(team)
ssh_password = hashlib.sha256("m0lehouse".encode()+password.encode()).hexdigest()
subdomain = hashlib.sha256("m0lehouseweb".encode()+password.encode()).hexdigest()[:16]
webpassword = hashlib.sha256("m0lehousewebpassword".encode()+password.encode()).hexdigest()[:16]

print(f"You can connect with ssh at {subdomain}.m0lehouse.challs.m0lecon.it with username root and pasword {ssh_password} at port {ssh_port}")
print(f"You can connect to the web interface at https://{subdomain}.m0lehouse.challs.m0lecon.it with basic auth credentials root:{webpassword}")