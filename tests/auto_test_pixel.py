from pathlib import Path
import cv2
import numpy as np

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Paths
INPUT_DIR = Path(r"C:\Users\marmo\OneDrive\Documents\auto-image-processor\input_images")
PIXELATED_DIR = Path(r"C:\Users\marmo\OneDrive\Documents\auto-image-processor\output_images\pixelated")

MIN_COLOR_REDUCTION = 0.9  # Pixelated image should have <90% of original unique colors


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS


def find_pixelated_file(stem: str) -> Path | None:
    """
    Find corresponding pixelated image by stem name
    """
    for f in PIXELATED_DIR.iterdir():
        if is_image_file(f) and f.stem == stem:
            return f
    return None


def is_pixelated(original_path: Path, pixelated_path: Path) -> bool:
    """
    Returns True if pixelated_path is likely a pixelated version of original_path
    """
    orig = cv2.imread(str(original_path))
    pix = cv2.imread(str(pixelated_path))

    if orig is None or pix is None:
        raise ValueError(f"Cannot read images: {original_path}, {pixelated_path}")

    # Resize pixelated to original if needed
    if orig.shape != pix.shape:
        pix = cv2.resize(pix, (orig.shape[1], orig.shape[0]))

    # Flatten and count unique colors
    orig_colors = np.unique(orig.reshape(-1, 3), axis=0)
    pix_colors = np.unique(pix.reshape(-1, 3), axis=0)

    # Pixelated image should have fewer unique colors
    if len(pix_colors) < len(orig_colors) * MIN_COLOR_REDUCTION:
        return True
    else:
        return False


def main():
    if not INPUT_DIR.exists():
        print(f"❌ input_images folder not found: {INPUT_DIR}")
        return

    if not PIXELATED_DIR.exists():
        print(f"❌ pixelated folder not found: {PIXELATED_DIR}")
        return

    images = [f for f in INPUT_DIR.iterdir() if is_image_file(f)]

    print("🟦 Pixelation Verification\n")

    for img in images:
        try:
            pixelated_file = find_pixelated_file(img.stem)
            if pixelated_file is None:
                print(f"{img.name} | ❌ pixelated file not found")
                continue

            if is_pixelated(img, pixelated_file):
                print(f"{img.name} | DONE ✅")
            else:
                print(f"{img.name} | ❌ NOT PIXELATED")

        except Exception as e:
            print(f"{img.name} | ❌ {e}")

    print("\n✅ Pixelation check finished")


if __name__ == "__main__":
    main()
