import sys
import os
from stringcompare import compString


def main():
    if len(sys.argv) < 3:
        print("In following format:")
        print("    \"prifix\" -time/name")
        return False

    if len(sys.argv) == 4:
        startnum = int(sys.argv[3])
    else:
        startnum = 0

    prifix = sys.argv[1]
    method = sys.argv[2]

    orifiles = os.listdir()
    orifiles.remove(sys.argv[0])
    newlist = orifiles.copy()

    if method == "-name":
        newlist.sort(key=compString)
    elif method == "-time":
        newlist.sort(key=os.path.getmtime)
    else:
        print("Use following parameter:")
        print("  -time")
        print("  -name")
        return False

    print("new order will be:")
    for i in range(0, len(newlist)):
        print(newlist[i])
    answer = input("Continue y/n?")
    if answer == 'n':
        return False

    i = startnum
    for file in newlist:
        ext = os.path.splitext(file)[1]
        os.rename(file, prifix + "%04d" % i + ext)
        i = i + 1


if __name__ == "__main__":
    sys.exit(main())
