from pathlib import Path
from shutil import rmtree

# Wipe all compressed images from the image directory
def main():
    images = Path("images")

    for dir in images.iterdir():
        if dir.name != "original":
            rmtree(dir)


if __name__ == "__main__":
    main()
