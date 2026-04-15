from util import png_to_jpeg, IMAGES_PATH, ORIGINAL_IMAGES_PATH

# Compress original images at different jpeg qualities
def main():

    if not ORIGINAL_IMAGES_PATH.exists() or not ORIGINAL_IMAGES_PATH.is_dir():
        raise OSError("Directory of original images does not exist.")

    qualities = [1, 10, 25, 50, 75, 95]

    for quality in qualities:
        qdir = IMAGES_PATH / f"{quality}"
        qdir.mkdir(exist_ok=True)

        for original_img in ORIGINAL_IMAGES_PATH.iterdir():
            if original_img.is_file() and original_img.suffix == ".png":
                png_to_jpeg(
                    original_img, qdir / f"{original_img.stem}.jpg", quality
                )


if __name__ == "__main__":
    main()
