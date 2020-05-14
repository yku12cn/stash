import sys
from pathlib import Path
from PIL import Image

_Ftable = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]


def main():
    orifiles = sorted(list(Path("./").glob("*")))
    # remove this script from target list
    orifiles.remove(Path(Path(sys.argv[0]).name))
    for file in orifiles:
        if file.is_dir():  # jump over dir
            continue
        # Check extention
        if file.suffix.lower() not in _Ftable:
            continue
        try:
            im = Image.open(file)
        except IOError:
            print(file.name, "is not an image")
            continue

        if im.format == "JPEG":  # check if jpg file is correct
            if file.suffix.lower() in [".jpg", ".jpeg"]:
                # if file name matches its format
                im.close()
                continue
            else:
                # correct file name
                print(file.name, "should be .jpg")
                im.close()
                file.rename(file.stem + ".jpg")
                continue

        if im.format == "PNG":  # Process png files
            print(file.name, ":", im.format, im.mode)
            if im.mode == "RGBA" or im.mode == "P":
                im = im.convert("RGB")
            if im.mode == "LA":
                im = im.convert("L")
            im.save(file.stem + ".jpg", quality=95)
            im.close()
            if file.suffix != ".jpg":
                file.unlink()
        else:
            im.close()

    input('Done')


if __name__ == "__main__":
    sys.exit(main())
