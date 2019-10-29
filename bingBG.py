from SimpleWeb import SimpleWeb
from setWallPaper import setWallPaper
import sys
import os
import re


def main():
    bingurl = 'https://www.bing.com'
    bgfile = os.environ["userprofile"] + '\\Pictures\\bingBG\\'

    if not os.path.exists(bgfile):
        os.makedirs(bgfile)

    web = SimpleWeb()
    out = web.reqCode(bingurl)  # Get target code
    web.updateNetloc()

    # Search for all links
    test = re.findall(r"g_img\=\{url.*?\"(.*?)\\", out)
    imgurl = ''
    for a in test:
        if '1920x1080' in a:
            imgurl = a
            break
    if imgurl == '':
        print('Not found')
    else:
        print(imgurl)

    # Extract file name
    filename = re.findall(r"([^.]*?\.[^.]*?)$", imgurl)[0]
    print(filename)

    # Download file
    web.saveFile(imgurl, bgfile + filename)

    # Setting Wallpapper
    bgfile += filename

    setWallPaper(bgfile)


if __name__ == "__main__":
    sys.exit(main())
