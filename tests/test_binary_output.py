from pathlib import Path
import pytest
import cv2
import numpy as np

from src.binary import to_binary
from src.image_compression import is_image_file  # reuse your helper


# Project root relative to this test file
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_DIR = PROJECT_ROOT / "input_images"
OUTPUT_DIR = PROJECT_ROOT / "output_images" / "binary"


@pytest.mark.parametrize("img_path", list(INPUT_DIR.iterdir()))
def test_binary_output(img_path):
    # Skip non-image files
    if not is_image_file(img_path):
        pytest.skip(f"{img_path.name} is not an image file, skipping binary test")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---------- Default threshold ----------
    default_out = OUTPUT_DIR / f"{img_path.stem}_default.png"
    to_binary(img_path, default_out)
    assert default_out.exists(), "Binary output file not created (default threshold)"

    img_default = cv2.imread(str(default_out), cv2.IMREAD_GRAYSCALE)
    assert img_default is not None, "Failed to read binary output (default threshold)"

    unique_vals = set(np.unique(img_default))
    assert unique_vals.issubset({0, 255}), \
        f"Image contains non-binary values (default threshold): {unique_vals}"


    # ---------- Low threshold ----------
    low_out = OUTPUT_DIR / f"{img_path.stem}_low.png"
    to_binary(img_path, low_out, threshold=0)
    assert low_out.exists()

    img_low = cv2.imread(str(low_out), cv2.IMREAD_GRAYSCALE)
    unique_low = set(np.unique(img_low))
    assert unique_low.issubset({0, 255}), \
        f"Image contains non-binary values (low threshold): {unique_low}"


    # ---------- High threshold ----------
    high_out = OUTPUT_DIR / f"{img_path.stem}_high.png"
    to_binary(img_path, high_out, threshold=255)
    assert high_out.exists()

    img_high = cv2.imread(str(high_out), cv2.IMREAD_GRAYSCALE)
    unique_high = set(np.unique(img_high))
    assert unique_high.issubset({0, 255}), \
        f"Image contains non-binary values (high threshold): {unique_high}"


    # ---------- Error handling ----------
    fake_file = INPUT_DIR / "nonexistent.jpg"
    with pytest.raises(FileNotFoundError):
        to_binary(fake_file, OUTPUT_DIR / "fake.png")
