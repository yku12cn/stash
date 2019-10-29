def _mycomp(a, b, inda=0, indb=0):
    # Check if empty
    if len(a) == inda:
        return False
    else:
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
            else:
                return inta > intb
        else:
            # a < b given a is digit while b is not
            return False
    else:
        if b[indb].isdigit():
            # a > b given a is not digit while b is
            return True
        else:
            # Both are non digit
            if a[inda] == b[indb]:
                return _mycomp(a, b, inda + 1, indb + 1)
            else:
                return a[inda] > b[indb]


class compString(str):
    # An workaround for "key" sort in Python3.x
    def __gt__(a, b):
        return _mycomp(a, b)

    def __lt__(a, b):
        return not _mycomp(a, b)


if __name__ == "__main__":
    sample = ["b-23", "asds-23", "csds-23"]
    print(sorted(sample, key=compString))
