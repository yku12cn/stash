"""
    Compress images
"""
import sys
import os
import shutil
from pathlib import PurePath
from pathlib import Path

import tqdm
import cv2


def ImgCompresser(filename, output, quality=0.75):
    im = cv2.imread(filename, 1)  # load image as RGB
    if im is None:
        return
    ext = (PurePath(output).suffix).lower()
    if ("jpg" in ext) or ("jpeg" in ext):
        cv2.imwrite(output, im,
                    [int(cv2.IMWRITE_JPEG_QUALITY), 100 * quality])

    elif "png" in ext:
        cv2.imwrite(output, im,
                    [int(cv2.IMWRITE_PNG_COMPRESSION), 9 * (1 - quality)])

    else:  # No compression for others
        shutil.copy(filename, output)


def main():
    if len(sys.argv) == 1:
        inputF = input("Source folder:")
        if not inputF:
            inputF = Path("./")
        else:
            inputF = Path(inputF)

        outputF = input("Output folder:")
        if not outputF:
            outputF = Path("./output/")
        else:
            outputF = Path(outputF)

        quality = input("Quality 0.0-1.0:")
        try:
            quality = float(quality)
        except ValueError:
            quality = 0.85

    else:
        if len(sys.argv) != 4:
            print("Usage:")
            print("   python %s \"input folder\" \"output folder\" 0.85" %
                  (sys.argv[0]))
            return

        inputF = Path(sys.argv[1])
        outputF = Path(sys.argv[2])
        quality = float(sys.argv[3])

    if not outputF.exists():
        outputF.mkdir(parents=True)

    if not (inputF.exists() and inputF.is_dir()):
        print("error input parameter")

    imglist = sorted(list(inputF.glob("*")))

    system = (os.name == "nt")
    t = tqdm.trange(len(imglist), desc="Current: ", leave=True, ascii=system)
    for file in imglist:
        t.set_description("Current: %s" % (file.name))
        # t.refresh()
        t.update()
        # t.write(file.name)
        ImgCompresser(str(file), str(outputF / file.name), quality=quality)
    t.close()


if __name__ == "__main__":
    sys.exit(main())
