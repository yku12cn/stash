import hashlib
import requests
import getpass
import sys


pauseflag = False

if len(sys.argv) == 2:
    testword = sys.argv[1]
else:
    testword = getpass.getpass("Input your password: ")
    pauseflag = True

sha1Hash = hashlib.sha1(testword.encode('utf-8')).hexdigest().upper()
sha1HashH, sha1HashT = sha1Hash[:5], sha1Hash[5:]

res = requests.get('https://api.pwnedpasswords.com/range/' + sha1HashH)

hashes = (line.split(':') for line in res.text.splitlines())
count = next((int(count) for t, count in hashes if t == sha1HashT), 0)

if count == 0:
    print("No leak")
else:
    print(testword, "was found")
    print("Hash", sha1Hash, ",", count, "occurences")

if pauseflag:
    input("Done")
