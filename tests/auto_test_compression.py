# auto_test/auto_test_compression.py

from pathlib import Path
import cv2
import os
from src.image_compression import compress_image, is_image_file

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_DIR = PROJECT_ROOT / "input_images"
OUTPUT_DIR = PROJECT_ROOT / "output_images/compressed"

JPEG_QUALITY = 60  # same as your main.py

# Ensure folders exist
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def format_size(bytes_size):
    """Convert bytes to KB or MB string"""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024*1024:
        return f"{bytes_size/1024:.1f} KB"
    else:
        return f"{bytes_size/(1024*1024):.2f} MB"


def test_auto_compression():
    images = [f for f in INPUT_DIR.iterdir() if is_image_file(f)]

    if not images:
        print("No images found in input folder.")
        return

    for image in images:
        input_path = image
        output_path = OUTPUT_DIR / image.name

        # Read original image for size info
        img_orig = cv2.imread(str(input_path))
        if img_orig is None:
            print(f"Skipping {image.name}: cannot read original")
            continue

        orig_h, orig_w = img_orig.shape[:2]
        orig_file_size = os.path.getsize(input_path)

        # Compress image using main.py function
        compress_image(input_path, output_path, quality=JPEG_QUALITY)

        # Get compressed file size
        if not output_path.exists():
            print(f"Failed to compress {image.name}")
            continue

        comp_file_size = os.path.getsize(output_path)
        size_reduction = 100 * (orig_file_size - comp_file_size) / orig_file_size

        # Print info to terminal
        print(
            f"{image.name}: {orig_w}x{orig_h} "
            f"→ {orig_w}x{orig_h} | "
            f"Size: {format_size(orig_file_size)} → {format_size(comp_file_size)} "
            f"({size_reduction:.1f}% reduction) ✅"
        )

    print(f"\nAll images processed: {len(images)} files")


if __name__ == "__main__":
    test_auto_compression()
