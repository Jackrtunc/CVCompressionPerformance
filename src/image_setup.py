from util import *
from pathlib import Path


# Compress original images at different jpeg qualities
def main():
    images = Path("images")
    original = images / "original"

    if not original.exists() or not original.is_dir():
        raise OSError("Directory of original images does not exist.")

    qualities = [1, 10, 25, 50, 75, 95]

    for quality in qualities:
        qdir = images / f"q{quality}"
        qdir.mkdir(exist_ok=True)

        for original_img in original.iterdir():
            if original_img.is_file() and original_img.suffix == ".png":
                png_to_jpeg(
                    original_img, qdir / f"{original_img.stem}_{quality}.jpg", quality
                )


if __name__ == "__main__":
    main()
