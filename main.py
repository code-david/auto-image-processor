from pathlib import Path
import sys

from src.image_compression import compress_image, is_image_file
from src.pixelation import pixelate_image
from src.binary import to_binary
from src.resizing import resize_image
from src.color_inversion import invert_colors   

INPUT_DIR = Path("input_images")

OUT_COMPRESSED = Path("output_images/compressed")
OUT_PIXELATED = Path("output_images/pixelated")
OUT_BINARY = Path("output_images/binary")
OUT_RESIZED = Path("output_images/resized")
OUT_INVERTED = Path("output_images/inverted")   

DEFAULT_QUALITY = 60
DEFAULT_PIXEL_SIZE = 16
DEFAULT_THRESHOLD = 128
DEFAULT_W = 100
DEFAULT_H = 100


def usage():
    print("Usage:")
    print("  python main.py compress [quality]")
    print("  python main.py pixelate [pixel_size]")
    print("  python main.py binary [threshold]")
    print("  python main.py resize [width height]")
    print("  python main.py invert")   
    print("")
    print("Examples:")
    print("  python main.py")
    print("  python main.py compress 60")
    print("  python main.py pixelate 16")
    print("  python main.py binary 128")
    print("  python main.py resize 100 100")
    print("  python main.py invert")   


def list_input_images():
    INPUT_DIR.mkdir(exist_ok=True)
    return [p for p in INPUT_DIR.iterdir() if is_image_file(p)]


def run_compress(images, quality: int):
    OUT_COMPRESSED.mkdir(parents=True, exist_ok=True)
    for img in images:
        out_path = (OUT_COMPRESSED / img.stem).with_suffix(".jpg")
        compress_image(img, out_path, quality=quality)
        print(f"Compressed: {img.name}")


def run_pixelate(images, pixel_size: int):
    OUT_PIXELATED.mkdir(parents=True, exist_ok=True)
    for img in images:
        out_path = OUT_PIXELATED / img.name
        pixelate_image(img, out_path, pixel_size=pixel_size)
        print(f"Pixelated: {img.name}")


def run_binary(images, threshold: int):
    OUT_BINARY.mkdir(parents=True, exist_ok=True)
    for img in images:
        out_path = OUT_BINARY / img.name
        to_binary(img, out_path, threshold=threshold)
        print(f"Binary: {img.name} (threshold={threshold})")


def run_resize(images, width: int, height: int):
    OUT_RESIZED.mkdir(parents=True, exist_ok=True)
    for img in images:
        out_path = OUT_RESIZED / img.name
        resize_image(img, out_path, width=width, height=height)
        print(f"Resized: {img.name} -> {width}x{height}")

def run_invert(images):
    OUT_INVERTED.mkdir(parents=True, exist_ok=True)
    for img in images:
        out_path = OUT_INVERTED / img.name
        invert_colors(img, out_path)
        print(f"Inverted: {img.name}")


def main():
    images = list_input_images()

    if not images:
        print("No images found in input_images/")
        return

    if len(sys.argv) < 2:
        run_compress(images, DEFAULT_QUALITY)
        run_pixelate(images, DEFAULT_PIXEL_SIZE)
        run_binary(images, DEFAULT_THRESHOLD)
        run_resize(images, DEFAULT_W, DEFAULT_H)
        run_invert(images)   
        return

    mode = sys.argv[1].lower()
    images = list_input_images()

    if mode == "compress":
        q = DEFAULT_QUALITY
        if len(sys.argv) >= 3:
            try:
                q = int(sys.argv[2])
            except ValueError:
                pass
        run_compress(images, max(0, min(100, q)))

    elif mode == "pixelate":
        p = DEFAULT_PIXEL_SIZE
        if len(sys.argv) >= 3:
            try:
                p = int(sys.argv[2])
            except ValueError:
                pass
        run_pixelate(images, max(1, p))

    elif mode == "binary":
        t = DEFAULT_THRESHOLD
        if len(sys.argv) >= 3:
            try:
                t = int(sys.argv[2])
            except ValueError:
                pass
        run_binary(images, max(0, min(255, t)))

    elif mode == "resize":
        w, h = DEFAULT_W, DEFAULT_H
        if len(sys.argv) >= 4:
            try:
                w = int(sys.argv[2])
                h = int(sys.argv[3])
            except ValueError:
                pass
        run_resize(images, max(1, w), max(1, h))

    elif mode == "invert":
        run_invert(images)

    else:
        usage()
        
if __name__ == "__main__":
    main()
