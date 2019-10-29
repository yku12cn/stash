import sys
import os
from checkimage import ckimg
from setWallPaper import setWallPaper
from shutil import copyfile
import win32api


def main():
    filebase = os.environ["userprofile"]
    Original_File = filebase + "\\AppData\\Local\\Packages\\\
Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\\
LocalState\\Assets\\"

    Horizontal_Location = filebase + "\\Pictures\\Spotlight\\Horizontal\\"
    Vertical_Location = filebase + "\\Pictures\\Spotlight\\Vertical\\"

    Vertical_Flag = win32api.GetSystemMetrics(1) > win32api.GetSystemMetrics(0)

    bgfile = Vertical_Location if Vertical_Flag else Horizontal_Location

    if not os.path.exists(bgfile):
        os.makedirs(bgfile)

    templist = os.listdir(Original_File)
    for i in range(len(templist)):
        templist[i] = Original_File + templist[i]

    templist.sort(key=os.path.getmtime, reverse=True)

    for item in templist:  # Get latest qualified image
        if os.path.getsize(item) < 200000:
            continue
        T, W, H, _ = ckimg(item)
        if Vertical_Flag == (H > W):
            print(os.path.getsize(item), (W, H, T), os.path.split(item)[1])
            bgfile += os.path.split(item)[1] + "." + T
            copyfile(item, bgfile)
            break

    setWallPaper(bgfile)


if __name__ == "__main__":
    sys.exit(main())
