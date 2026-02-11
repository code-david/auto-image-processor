from pathlib import Path
import pytest
from src.image_compression import compress_image, is_image_file

# Project root relative to this test file
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_DIR = PROJECT_ROOT / "input_images"
OUTPUT_DIR = PROJECT_ROOT / "output_images" / "compressed"

JPEG_QUALITY = 60  # default quality for tests


@pytest.mark.parametrize("img_path", list(INPUT_DIR.iterdir()))
def test_compression_output(img_path):
    # Skip non-image files
    if not is_image_file(img_path):
        pytest.skip(f"{img_path.name} is not an image file, skipping compression test")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"{img_path.stem}.jpg"

    # Normal compression
    compress_image(img_path, out_file, quality=JPEG_QUALITY)
    assert out_file.exists(), f"Output file not created: {out_file}"

    # Extreme qualities
    compress_image(img_path, out_file, quality=0)
    assert out_file.exists()
    compress_image(img_path, out_file, quality=100)
    assert out_file.exists()

    # Check error handling
    fake_file = INPUT_DIR / "nonexistent.jpg"
    with pytest.raises(FileNotFoundError):
        compress_image(fake_file, OUTPUT_DIR / "fake.jpg")
