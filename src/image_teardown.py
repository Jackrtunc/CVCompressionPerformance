from shutil import rmtree
from util import IMAGES_PATH, ORIGINAL_IMAGES_NAME


# Wipe all compressed images from the image directory
def main():
    for dir in IMAGES_PATH.iterdir():
        if dir.name != ORIGINAL_IMAGES_NAME:
            rmtree(dir)


if __name__ == "__main__":
    main()
