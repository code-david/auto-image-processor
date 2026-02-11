from pathlib import Path
import pytest
from src.resizing import resize_image

# Project root relative to this test file
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_DIR = PROJECT_ROOT / "input_images"
OUTPUT_DIR = PROJECT_ROOT / "output_images" / "resized"

# Default resize dimensions for tests
DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 100


@pytest.mark.parametrize("img_path", list(INPUT_DIR.iterdir()))
def test_resize_output(img_path):
    """
    Professional behavior test for image resizing:
    - Skips non-image files
    - Tests default resizing
    - Tests custom sizes
    - Checks missing file error
    """

    # Only test image files
    if img_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}:
        pytest.skip(f"{img_path.name} is not an image file, skipping resize test")

    # Ensure output folder exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # Test 1: Default resize
    # -----------------------------
    out_default = OUTPUT_DIR / f"{img_path.stem}_default.jpg"
    resize_image(img_path, out_default)
    assert out_default.exists(), f"Default resized file not created: {out_default}"

    # -----------------------------
    # Test 2: Custom resize
    # -----------------------------
    custom_width, custom_height = 200, 150
    out_custom = OUTPUT_DIR / f"{img_path.stem}_custom.jpg"
    resize_image(img_path, out_custom, width=custom_width, height=custom_height)
    assert out_custom.exists(), f"Custom resized file not created: {out_custom}"

    # -----------------------------
    # Test 3: Missing file error
    # -----------------------------
    fake_file = INPUT_DIR / "nonexistent.jpg"
    with pytest.raises(FileNotFoundError):
        resize_image(fake_file, OUTPUT_DIR / "fake.jpg")
