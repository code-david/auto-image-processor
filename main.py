from pathlib import Path
from src.image_compression import compress_image, is_image_file

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output/compressed")
JPEG_QUALITY = 60  # lower = more compression


def main():
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    images = [f for f in INPUT_DIR.iterdir() if is_image_file(f)]

    if not images:
        print("No images found in input folder.")
        return

    for image in images:
        output_path = OUTPUT_DIR / image.name
        compress_image(image, output_path, quality=JPEG_QUALITY)
        print(f"Compressed: {image.name}")

    print("Image compression completed.")


if __name__ == "__main__":
    main()
