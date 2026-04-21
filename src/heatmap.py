from util import *

def main():
    save_depth_heatmap(get_depth_map(IMAGES_PATH / "95/0801.jpg", get_model("vitl")), Path("heatmap-95.jpg"))

if __name__ == "__main__":
    main()