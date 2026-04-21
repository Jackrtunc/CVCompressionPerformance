import cv2
import numpy as np
import torch
from depth_anything_v2.depth_anything_v2.dpt import DepthAnythingV2
from pathlib import Path
from PIL import Image

IMAGES_PATH = Path("images")
ORIGINAL_IMAGES_NAME = "original"
ORIGINAL_IMAGES_PATH = IMAGES_PATH / ORIGINAL_IMAGES_NAME
RESULTS_PATH = Path("results")


# We're using the vitl model
def get_model(encoder: str) -> DepthAnythingV2:
    model_configs = {
        "vits": {"encoder": "vits", "features": 64, "out_channels": [48, 96, 192, 384]},
        "vitb": {
            "encoder": "vitb",
            "features": 128,
            "out_channels": [96, 192, 384, 768],
        },
        "vitl": {
            "encoder": "vitl",
            "features": 256,
            "out_channels": [256, 512, 1024, 1024],
        },
        "vitg": {
            "encoder": "vitg",
            "features": 384,
            "out_channels": [1536, 1536, 1536, 1536],
        },
    }

    if encoder not in model_configs:
        raise ValueError(
            f"Encoder {encoder} not supported. Supported encoders: {list(model_configs.keys())}."
        )

    DEVICE = (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )

    model = DepthAnythingV2(**model_configs[encoder])
    model.load_state_dict(
        torch.load(f"checkpoints/depth_anything_v2_{encoder}.pth", map_location="cpu")
    )
    model = model.to(DEVICE).eval()

    return model


def get_depth_map(img_path: Path, model: DepthAnythingV2) -> np.ndarray:
    img_array = cv2.imread(img_path)
    if img_array is None:
        raise FileNotFoundError(f"Could not read image {img_path}.")
    return model.infer_image(img_array)


def png_to_jpeg(input_path: Path, output_path: Path, quality: int) -> None:
    if quality not in range(1, 96):
        raise ValueError(f"Quality must be between 1 and 95.")
    img = Image.open(input_path)
    img.save(output_path, format="JPEG", quality=quality)


def save_depth_heatmap(
    img_depth: np.ndarray, output_path: Path, colormap: int = cv2.COLORMAP_TURBO
) -> None:
    depth_min = img_depth.min()
    depth_max = img_depth.max()
    depth_range = depth_max - depth_min

    if depth_range == 0:
        normalized = np.zeros_like(img_depth, dtype=np.uint8)
    else:
        normalized = ((img_depth - depth_min) / depth_range * 255).astype(np.uint8)

    colored_bgr = cv2.applyColorMap(normalized, colormap)
    colored_rgb = cv2.cvtColor(colored_bgr, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(colored_rgb)
    img.save(output_path, format="PNG")


# Normalized mean absolute error
def calculate_nmae(baseline: np.ndarray, compressed: np.ndarray) -> float:
    difference = baseline - compressed
    mae = np.mean(np.abs(difference))
    baseline_range = baseline.max() - baseline.min()
    return mae / baseline_range


# Normalized root mean squared error
def calculate_nrmse(baseline: np.ndarray, compressed: np.ndarray) -> float:
    difference = baseline - compressed
    rmse = np.sqrt(np.mean(difference**2))
    baseline_range = baseline.max() - baseline.min()
    return rmse / baseline_range
