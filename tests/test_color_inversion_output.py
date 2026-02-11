from pathlib import Path
import pytest
import cv2
import numpy as np

from src.color_inversion import invert_colors
from src.image_compression import is_image_file  # optional helper to skip non-images

# Project root relative to this test file
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_DIR = PROJECT_ROOT / "input_images"
OUTPUT_DIR = PROJECT_ROOT / "output_images" / "inverted"  # <- updated folder


@pytest.mark.parametrize("img_path", list(INPUT_DIR.iterdir()))
def test_color_inversion_output(img_path):
    # Skip non-image files
    if not is_image_file(img_path):
        pytest.skip(f"{img_path.name} is not an image file, skipping color inversion test")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Output path
    out_file = OUTPUT_DIR / f"{img_path.stem}_inverted.png"

    # Apply color inversion
    invert_colors(img_path, out_file)

    # Check that the output file exists
    assert out_file.exists(), "Color inverted output file was not created"

    # Load original and inverted images
    original = cv2.imread(str(img_path))
    inverted = cv2.imread(str(out_file))
    assert original is not None, f"Failed to read original {img_path.name}"
    assert inverted is not None, f"Failed to read inverted {out_file.name}"

    # ---------- Pixel check ----------
    # Sum of original + inverted ≈ 255 for each channel
    summed = original.astype(np.int16) + inverted.astype(np.int16)
    assert np.all((summed >= 254) & (summed <= 256)), \
        f"Inverted image pixels are not correct for {img_path.name}"

    # ---------- Error handling ----------
    fake_file = INPUT_DIR / "nonexistent.jpg"
    with pytest.raises(FileNotFoundError):
        invert_colors(fake_file, OUTPUT_DIR / "fake.png")
