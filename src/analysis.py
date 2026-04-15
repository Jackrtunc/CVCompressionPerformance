from util import *
import csv


def main():
    with open(RESULTS_PATH / "analysis.csv", "w", newline="") as f:
        writer = csv.writer(f)
        model = get_model("vitl")

        baselines = [{img.stem: get_depth_map(img, model)} for img in ORIGINAL_IMAGES_PATH.iterdir() if img.suffix == ".png"]


        for dir in IMAGES_PATH.iterdir():
            if dir.name != ORIGINAL_IMAGES_NAME:
                quality = int(dir.name)

                if quality not in range(1, 96):
                    raise ValueError("Found invalid quality directory")
                


if __name__ == "__main__":
    main()
