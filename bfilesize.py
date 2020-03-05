"""Quickly translate file size in bytes to KB/MB/GB/TB
Copyright 2020 Yang Kaiyu yku12cn@gmail.com
"""

__unit = ["byte", "KB", "MB", "GB", "TB"]


def bFSize(fsize=0):
    """Input file size measured in bytes
    returns a string for display purpose
    """
    nsize = fsize / 1024
    i = 0
    while i < 4:
        if nsize < 1:
            break
        fsize = nsize
        nsize = fsize / 1024
        i = i + 1
    return "%.4g %s" % (fsize, __unit[i])


if __name__ == "__main__":
    print(bFSize(102938552))
