from pathlib import Path
import sys

from src.image_compression import compress_image, is_image_file

INPUT_DIR = Path("input_images")
OUTPUT_DIR = Path("output_images/compressed")

DEFAULT_QUALITY = 60


def main():
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # optional: python main.py 60
    quality = DEFAULT_QUALITY
    if len(sys.argv) >= 2:
        try:
            quality = int(sys.argv[1])
        except ValueError:
            pass

    images = [p for p in INPUT_DIR.iterdir() if is_image_file(p)]
    if not images:
        print("No images found in input_images/")
        return

    for img_path in images:
        out_path = OUTPUT_DIR / img_path.stem
        out_path = out_path.with_suffix(".jpg")  # always save as jpg
        compress_image(img_path, out_path, quality=quality)
        print(f"Compressed: {img_path.name} -> {out_path.name} (quality={quality})")

    print("Image compression completed.")


if __name__ == "__main__":
    main()
