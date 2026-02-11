from pathlib import Path
import pytest
import cv2
import numpy as np

from src.pixelation import pixelate_image
from src.image_compression import is_image_file  # reuse your helper

# Project root relative to this test file
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_DIR = PROJECT_ROOT / "input_images"
OUTPUT_DIR = PROJECT_ROOT / "output_images" / "pixelated"

DEFAULT_PIXEL_SIZE = 16  # matches main.py

@pytest.mark.parametrize("img_path", list(INPUT_DIR.iterdir()))
def test_pixelation_output(img_path):
    # Skip non-image files
    if not is_image_file(img_path):
        pytest.skip(f"{img_path.name} is not an image file")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Default pixelation
    default_file = OUTPUT_DIR / f"{img_path.stem}_default.png"
    pixelate_image(img_path, default_file, pixel_size=DEFAULT_PIXEL_SIZE)
    assert default_file.exists(), f"Default pixelated image not created: {default_file}"

    # Custom pixelation
    custom_pixel_size = 32
    custom_file = OUTPUT_DIR / f"{img_path.stem}_custom.png"
    pixelate_image(img_path, custom_file, pixel_size=custom_pixel_size)
    assert custom_file.exists(), f"Custom pixelated image not created: {custom_file}"

    # Load original and pixelated images
    orig_img = cv2.imread(str(img_path))
    default_img = cv2.imread(str(default_file))
    custom_img = cv2.imread(str(custom_file))

    assert orig_img is not None
    assert default_img is not None
    assert custom_img is not None

    # Ensure the pixelated images have same dimensions as original
    assert default_img.shape[:2] == orig_img.shape[:2]
    assert custom_img.shape[:2] == orig_img.shape[:2]

    # Optional: check that the pixelated images differ from original
    assert not np.array_equal(orig_img, default_img), "Default pixelation did not change image"
    assert not np.array_equal(orig_img, custom_img), "Custom pixelation did not change image"
