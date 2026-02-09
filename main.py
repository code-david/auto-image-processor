# main.py
import sys
from pathlib import Path

from src.image_compression import compress_image, is_image_file as is_image_file_compress
from src.pixelation import pixelate_image
from src.color_inversion import invert_colors
from src.binary import to_binary
from src.resizing import resize_image

# Folders (standard)
INPUT_DIR = Path("input_images")

OUT_COMPRESSED = Path("output_images/compressed")
OUT_PIXELATED = Path("output_images/pixelated")
OUT_INVERTED = Path("output_images/inverted")
OUT_BINARY = Path("output_images/binary")
OUT_RESIZED = Path("output_images/resized")

# Defaults
JPEG_QUALITY = 60
PIXEL_SIZE = 16
BINARY_THRESHOLD = 128
DEFAULT_W = 100
DEFAULT_H = 100


def usage():
    print("Usage:")
    print("  python main.py compress [quality]")
    print("  python main.py pixelate [pixel_size]")
    print("  python main.py invert")
    print("  python main.py binary [threshold]")
    print("  python main.py resize [width height]")
    print("")
    print("Examples:")
    print("  python main.py compress 60")
    print("  python main.py pixelate 20")
    print("  python main.py invert")
    print("  python main.py binary 150")
    print("  python main.py resize 100 100")


def list_input_images():
    INPUT_DIR.mkdir(exist_ok=True)
    # use one is_image_file implementation (from compression module)
    images = [f for f in INPUT_DIR.iterdir() if is_image_file_compress(f)]
    return images


def run_compress(images, quality: int):
    OUT_COMPRESSED.mkdir(parents=True, exist_ok=True)
    for image in images:
        out_path = OUT_COMPRESSED / image.name
        compress_image(image, out_path, quality=quality)
        print(f"Compressed: {image.name} (quality={quality})")
    print("Compression completed.")


def run_pixelate(images, pixel_size: int):
    OUT_PIXELATED.mkdir(parents=True, exist_ok=True)
    for image in images:
        out_path = OUT_PIXELATED / image.name
        pixelate_image(image, out_path, pixel_size=pixel_size)
        print(f"Pixelated: {image.name} (pixel_size={pixel_size})")
    print("Pixelation completed.")


def run_invert(images):
    OUT_INVERTED.mkdir(parents=True, exist_ok=True)
    for image in images:
        out_path = OUT_INVERTED / image.name
        invert_colors(image, out_path)
        print(f"Inverted: {image.name}")
    print("Inversion completed.")


def run_binary(images, threshold: int):
    OUT_BINARY.mkdir(parents=True, exist_ok=True)
    for image in images:
        out_path = OUT_BINARY / image.name
        to_binary(image, out_path, threshold=threshold)
        print(f"Binary: {image.name} (threshold={threshold})")
    print("Binary conversion completed.")


def run_resize(images, width: int, height: int):
    OUT_RESIZED.mkdir(parents=True, exist_ok=True)
    for image in images:
        out_path = OUT_RESIZED / image.name
        resize_image(image, out_path, width=width, height=height)
        print(f"Resized: {image.name} -> {width}x{height}")
    print("Resizing completed.")


def main():
    if len(sys.argv) < 2:
        usage()
        return

    mode = sys.argv[1].lower().strip()
    images = list_input_images()

    if not images:
        print("No images found in input_images folder.")
        return

    if mode == "compress":
        quality = JPEG_QUALITY
        if len(sys.argv) >= 3:
            try:
                quality = int(sys.argv[2])
            except ValueError:
                pass
        quality = max(0, min(100, quality))
        run_compress(images, quality)

    elif mode == "pixelate":
        pixel_size = PIXEL_SIZE
        if len(sys.argv) >= 3:
            try:
                pixel_size = int(sys.argv[2])
            except ValueError:
                pass
        pixel_size = max(1, pixel_size)
        run_pixelate(images, pixel_size)

    elif mode == "invert":
        run_invert(images)

    elif mode == "binary":
        threshold = BINARY_THRESHOLD
        if len(sys.argv) >= 3:
            try:
                threshold = int(sys.argv[2])
            except ValueError:
                pass
        threshold = max(0, min(255, threshold))
        run_binary(images, threshold)

    elif mode == "resize":
        width, height = DEFAULT_W, DEFAULT_H
        if len(sys.argv) >= 4:
            try:
                width = int(sys.argv[2])
                height = int(sys.argv[3])
            except ValueError:
                pass
        width = max(1, width)
        height = max(1, height)
        run_resize(images, width, height)

    else:
        usage()


if __name__ == "__main__":
    main()
