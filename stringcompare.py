"""A better string comparison method
"""


def _mycomp(a, b, inda=0, indb=0):
    """A better string comparison method"""
    # Check if empty
    if len(a) == inda:
        return False
    if len(b) == indb:
        return True

    if a[inda].isdigit():
        if b[indb].isdigit():
            # Both are digit
            ra = inda + 1
            rb = indb + 1
            # read the whole integer
            while ra != len(a) and a[ra].isdigit():
                ra += 1
            while rb != len(b) and b[rb].isdigit():
                rb += 1
            inta = int(a[inda:ra])
            intb = int(b[indb:rb])
            if inta == intb:
                return _mycomp(a, b, ra, rb)
            return inta > intb
        # a < b given a is digit while b is not
        return False
    if b[indb].isdigit():
        # a > b given a is not digit while b is
        return True
    # Both are non digit
    if a[inda].lower() == b[indb].lower():
        return _mycomp(a, b, inda + 1, indb + 1)
    return a[inda].lower() > b[indb].lower()


class compString(str):
    """An workaround for "key" sort in Python3.x"""
    def __gt__(self, b):
        return _mycomp(self, b)

    def __lt__(self, b):
        return not _mycomp(self, b)


if __name__ == "__main__":
    sample = ["11.png", "111.png", "1111.png", "XTU.png",
              "map.bmp", "Sketchpad.png"]
    print(sorted(sample, key=compString))
