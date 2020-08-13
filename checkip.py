#! /usr/bin/python3
import sys
import json
from SimpleWeb import SimpleWeb


def __checkipK(targetIP, web):
    out = web.reqCode(f"http://ip-api.com/json/{targetIP}")
    out = json.loads(out)
    location = f"{out['country']}, {out['regionName']}, {out['city']}"
    isp = out['isp']
    return [location, isp]


def checkip(targetIP):
    web = SimpleWeb()
    if isinstance(targetIP, str):
        return __checkipK(targetIP, web)
    elif isinstance(targetIP, list):
        results = []
        for a_ip in targetIP:
            results.append(__checkipK(a_ip, web))
        return results
    else:
        print("Input Error!", file=sys.stderr)
        return None


if __name__ == "__main__":
    sys.exit(checkip(sys.argv[1]))
