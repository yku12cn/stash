import sys
import os
from pathlib import Path
from stringcompare import compString


def main():
    if len(sys.argv) == 1:
        prifix = input("Input prefix:")
        if not prifix:
            prifix = "default_"

        method = input("Sort by name? type \'T\' by time:")
        if method == 'T':
            method = "-time"
        else:
            method = "-name"

        startnum = input("Start from:")
        try:
            startnum = int(startnum)
        except ValueError:
            startnum = 0

    else:
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

    orifiles = list(Path("./").glob("*"))
    # remove this script from target list
    orifiles.remove(Path(Path(sys.argv[0]).name))

    if method == "-name":
        orifiles.sort(key=compString)
    elif method == "-time":
        orifiles.sort(key=os.path.getmtime)
    else:
        print("Use following parameter:")
        print("  -time")
        print("  -name")
        return False

    print("new order will be:", method)
    for file in orifiles:
        print(file)
    answer = input("Continue y/n?")
    if answer == 'n':
        return False

    for file in orifiles:
        ext = file.suffix
        file.rename(prifix + "%04d" % startnum + ext)
        startnum = startnum + 1


if __name__ == "__main__":
    sys.exit(main())
