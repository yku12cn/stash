#! /usr/bin/python3

import subprocess
import sys
import re
from SimpleWeb import SimpleWeb
from checkip import __checkipK

comm = "mtr -w -m 50 " + sys.argv[1]
print("mtr running...")
stdoutdata = subprocess.check_output(comm, shell=True)
outlist = stdoutdata.decode("utf-8").splitlines()
print("check where")
web = SimpleWeb()
for ipitem in outlist:
    if "|--" in ipitem:
        ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ipitem)
        if ip:
            ip = ip[0]
            [location, isp] = __checkipK(ip, web)
            print(ipitem, "\t addr:", location, "\tISP:", isp)
        else:
            print(ipitem)
    else:
        print(ipitem)
