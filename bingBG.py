"""scrape current Bing background as wallpaper"""
import sys
import os
import re
from bs4 import BeautifulSoup as bs
from SimpleWeb import SimpleWeb
from setWallPaper import setWallPaper


def main():
    bingurl = 'https://www.bing.com'
    bgfile = os.environ["userprofile"] + '\\Pictures\\bingBG\\'

    if not os.path.exists(bgfile):
        os.makedirs(bgfile)

    web = SimpleWeb()
    out = web.reqCode(bingurl)  # Get target code
    soup = bs(out, "lxml")
    web.updateNetloc()

    # Search for image
    imgurl = None
    for link in soup.find_all("link"):
        if link.get("as") and "image" in link.get("as"):
            if "1920x1080" in link.get("href"):
                imgurl = link.get("href")

    if imgurl:
        imgurl = imgurl.replace("1920x1080", "UHD")
        print(imgurl)
    else:
        print("Image not found")

    # Extract file name
    filename = re.findall(r"([^\.]*?\.[^\.]{3}?)\&", imgurl)[0]
    print(filename)
    bgfile += filename

    # Download file
    web.saveFile(imgurl, bgfile)

    # Setting Wallpapper
    setWallPaper(bgfile)


if __name__ == "__main__":
    sys.exit(main())
