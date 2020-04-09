import cv2
import numpy as np
from pathlib import PurePath
from pathlib import Path
import sys
import os
import tqdm


def equalHist(filename, output, low=0.01, high=0.01, quality=0.75):
    im = cv2.imread(filename, 1)  # load image as RGB
    gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # get BW version
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256]).T[0]
    hist = hist / np.sum(hist)  # Normalize
    conv = 0  # Find low threshold
    lowcut = 0
    for value in hist:
        conv += value
        if conv < low:
            lowcut += 1
        else:
            break

    conv = 0  # Find high threshold
    totalcut = lowcut
    for value in hist[::-1]:
        conv += value
        if conv < high:
            totalcut += 1
        else:
            break

    im = im.astype("float64")
    im = im - lowcut
    np.clip((255 / (255 - totalcut)) * im, 0, 255, out=im)

    # cv2.imshow('image', np.uint8(im))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    ext = (PurePath(output).suffix).lower()
    if ("jpg" in ext) or ("jpeg" in ext):
        cv2.imwrite(output, np.uint8(im),
                    [int(cv2.IMWRITE_JPEG_QUALITY), 100 * quality])

    elif "png" in ext:
        cv2.imwrite(output, np.uint8(im),
                    [int(cv2.IMWRITE_PNG_COMPRESSION), 9 * (1 - quality)])

    else:  # No compression for others
        cv2.imwrite(output, np.uint8(im))


def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("   python %s \"input folder\" \"output folder\"" %
              (sys.argv[0]))
        return

    inputF = Path(sys.argv[1])
    outputF = Path(sys.argv[2])

    if not outputF.exists():
        outputF.mkdir()

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
        equalHist(str(file), str(outputF / file.name))
    t.close()


if __name__ == "__main__":
    sys.exit(main())
