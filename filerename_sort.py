import sys
from pathlib import Path
from stringcompare import compString
import re


def main():
    orifiles = list(Path("./").glob("*"))
    # remove this script from target list
    if Path(Path(sys.argv[0]).name) in orifiles:
        orifiles.remove(Path(Path(sys.argv[0]).name))
    orifiles.sort(key=compString)

    for orifile in orifiles:
        if orifile.is_dir():
            continue
        print("File: %s--> " % orifile.name, end="")
        filetype = orifile.suffix
        filename = orifile.stem
        filename_t = re.findall(r"([0-9]{1,}?)$", filename)
        if len(filename_t):
            filename_nt = "%04d" % int(filename_t[0])
            filename_t = filename_t[0]
        else:
            filename_nt = ""
            filename_t = ""
        filename_p = re.findall("(.*?)%s$" % filename_t, filename)
        if len(filename_p):
            filename_p = filename_p[0]
        else:
            filename_p = ""
        print(filename_p + filename_nt + filetype)
        orifile.rename(filename_p + filename_nt + filetype)


if __name__ == "__main__":
    sys.exit(main())
