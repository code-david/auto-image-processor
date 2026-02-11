from pathlib import Path
import sys

from src.image_compression import compress_image, is_image_file
from src.pixelation import pixelate_image

INPUT_DIR = Path("input_images")

OUT_COMPRESSED = Path("output_images/compressed")
OUT_PIXELATED = Path("output_images/pixelated")

DEFAULT_QUALITY = 60
DEFAULT_PIXEL_SIZE = 16


def usage():
    print("Usage:")
    print("  python main.py compress [quality]")
    print("  python main.py pixelate [pixel_size]")
    print("")
    print("Examples:")
    print("  python main.py compress 60")
    print("  python main.py pixelate 16")


def list_input_images():
    INPUT_DIR.mkdir(exist_ok=True)
    images = [p for p in INPUT_DIR.iterdir() if is_image_file(p)]
    return images


def run_compress(images, quality: int):
    OUT_COMPRESSED.mkdir(parents=True, exist_ok=True)
    for img_path in images:
        out_path = (OUT_COMPRESSED / img_path.stem).with_suffix(".jpg")
        compress_image(img_path, out_path, quality=quality)
        print(f"Compressed: {img_path.name} -> {out_path.name} (quality={quality})")


def run_pixelate(images, pixel_size: int):
    OUT_PIXELATED.mkdir(parents=True, exist_ok=True)
    for img_path in images:
        out_path = OUT_PIXELATED / img_path.name
        pixelate_image(img_path, out_path, pixel_size=pixel_size)
        print(f"Pixelated: {img_path.name} (pixel_size={pixel_size})")


def main():
    if len(sys.argv) < 2:
        images = list_input_images()
        if not images:
            print("No images found in input_images/")
            return
        run_compress(images, DEFAULT_QUALITY)
        run_pixelate(images, DEFAULT_PIXEL_SIZE)
        return

    mode = sys.argv[1].lower().strip()
    images = list_input_images()

    if not images:
        print("No images found in input_images/")
        return

    if mode == "compress":
        quality = DEFAULT_QUALITY
        if len(sys.argv) >= 3:
            try:
                quality = int(sys.argv[2])
            except ValueError:
                pass
        quality = max(0, min(100, quality))
        run_compress(images, quality)

    elif mode == "pixelate":
        pixel_size = DEFAULT_PIXEL_SIZE
        if len(sys.argv) >= 3:
            try:
                pixel_size = int(sys.argv[2])
            except ValueError:
                pass
        pixel_size = max(1, pixel_size)
        run_pixelate(images, pixel_size)

    else:
        usage()
        
if __name__ == "__main__":
    main()
