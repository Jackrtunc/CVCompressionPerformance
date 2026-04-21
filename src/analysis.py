from util import *
import csv


def main():
    with open(RESULTS_PATH / "analysis.csv", "w", newline="") as f:
        model = get_model("vitl")
        headers = ["id", "quality", "height", "width", "nmae", "nrmse"]
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        f.flush()

        baseline_depth_maps = {}
        for img in ORIGINAL_IMAGES_PATH.iterdir():
            if img.suffix == ".png":
                baseline_depth_maps[img.stem] = get_depth_map(img, model)
                print(f"Processing file {img.name} quality baseline")

        for dir in IMAGES_PATH.iterdir():
            if dir.name != ORIGINAL_IMAGES_NAME:
                quality = int(dir.name)

                if quality not in range(1, 96):
                    raise ValueError(f"Invalid quality subdirectory: {dir.name}.")

                for img in dir.iterdir():
                    if img.suffix != ".jpg":
                        raise ValueError(f"Invalid input file: {img.name}.")

                    print(f"Processing file {img.name} quality {quality}.")

                    id = img.stem
                    baseline_depth_map = baseline_depth_maps[id]
                    depth_map = get_depth_map(img, model)
                    height, width = depth_map.shape
                    nmae = calculate_nmae(baseline_depth_map, depth_map)
                    nrmse = calculate_nrmse(baseline_depth_map, depth_map)

                    writer.writerow(
                        {
                            "id": id,
                            "quality": quality,
                            "height": height,
                            "width": width,
                            "nmae": nmae,
                            "nrmse": nrmse,
                        }
                    )
                    f.flush()


if __name__ == "__main__":
    main()
