# Disclaimer

These are some mini tools I made. Quality unsure.

# Contents

## autoHist.py

Load all images from one folder and auto tune their exposure.

**Usage:** python3 autoHist.py /\*\*/input_folder/ /\*\*/output_folder/

## bfilesize.py

Quickly translate file size in bytes to KB/MB/GB/TB

**Demo:**

```python
from bfilesize import bFSize

print(bFSize(102938552))
```

## bingBG.py

Set your Win10 wallpaper to current Bing's background

**Usage #1**: double click

**Usage #2**: python3 bingBG.py

## checkimage.py

A simplified version of Paulo Scardine's [get\_image\_size](https://github.com/scardine/image_size)

## checkip.py

Lookup ip addresses from [ipip](https://en.ipip.net/ip.html)

**Usage #1:** python3 checkip.py 192.168.1.1

**Usage #2:**

```python
from checkip import checkip

ip_list = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
print(checkip(ip_list))

```

## checkpassword.py

Using this [database](https://api.pwnedpasswords.com) to check if your password is leaked

Password is checked locally, no worry about security.

## filerename.py

Rename all files under current folder as "name0000.txt" "name0001.txt" ... "name9999.txt"

You need to specify "prefix" and "order by name/time"

**Usage:** python3 filerename.py prefix_ -name

## filerename_sort.py

Rename all files under current folder from "txt1.txt" to "txt0001.txt"

For file's name not ended with a number, nothing will be changed.

**Usage:** double click

## IMGcompress.py

Load all images from one folder and compress them

**Usage #1:** python3 IMGcompress.py /\*\*/input_folder/ /\*\*/output_folder/ 0.85

**Usage #2:** double click

## mytrace.py

Trace and lookup all ips from [ipip](https://en.ipip.net/ip.html)

need linux and mtr

**Usage:** python3 mytrace.py 192.168.0.1

## png-jpg.py

Change all .png images under current folder to .jpg

**Usage:** double click

## printLog.py

A wrap of python's print() function. So it can save all prints to a log file.

added a helper function tStamp() which can generate a compact time string

**Demo:**

```python
from printLog import printLog, tStamp

printL = printLog("%s.log" % tStamp())

for i in range(10):
    printL("hello from iter", i, t=True, end="")
    printL(" balabala?")

```

## setWallPaper.py

Set a file as your Win10 wallpaper

**Demo:**

```python
from setWallPaper import setWallPaper

setWallPaper("/you/picture/wallpaper.jpg")

```

## SimplePlot.py

A simplified matplot api used to plot any function

**Demo:**

```python
from SimplePlot import draw

# For help:
draw()

# Draw function:
draw(lambda x: 1/x, [0.1, 2])

```

## SimpleWeb.py

A simple but rather robust class for navigating Internet

**Demo #1:**

```python
from SimpleWeb import SimpleWeb

web = SimpleWeb()
print(web.reqCode("https://en.ipip.net/ip.html", post={"ip": "192.168.0.1"}))

```

**Demo #2**, with logfile:

```python
from SimpleWeb import SimpleWeb

web = SimpleWeb("logfile.log")
web.mylog(web.reqCode("https://en.ipip.net/ip.html", post={"ip": "192.168.0.1"}))

```

## spotlightBG.py

Set your Win10 wallpaper to the latest spotlight picture.

**Usage:** double click

## stringcompare.py

A better implementation of how to compare two strings containing number.

**Example:**

Original sort: ["abc11def", "abc2def", "abc1def"] -> ["abc1def", "abc11def", "abc2def"]

stringcompare sort: ["abc11def", "abc2def", "abc1def"] -> ["abc1def", "abc2def", "abc11def"]

**Usage:**

```python
from stringcompare import compString

str_list = ["abc11def", "abc2def", "abc1def"]
str_list.sort(key=compString)
print(str_list)

```
