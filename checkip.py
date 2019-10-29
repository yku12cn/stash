#! /usr/bin/python3

from SimpleWeb import SimpleWeb
import sys
import re


def __checkipK(targetIP, web):
    out = web.reqCode("https://en.ipip.net/ip.html", post={"ip": targetIP})
    out = out.replace("\r", "").replace("\n", "")
    location = re.findall(r"Location\</td.*?style.*?\>(.*?)\<", out)
    if len(location) == 0:
        location = "NA"
    else:
        location = location[0]
    isp = re.findall(r"ISP\</td.*?style.*?\>(.*?)\<", out)
    if len(isp) == 0:
        isp = "NA"
    else:
        isp = isp[0]
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
