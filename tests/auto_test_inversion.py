from pathlib import Path
import cv2
import numpy as np

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

INPUT_DIR = Path(r"C:\Users\marmo\OneDrive\Documents\auto-image-processor\input_images")
INVERTED_DIR = Path(r"C:\Users\marmo\OneDrive\Documents\auto-image-processor\output_images\inverted")

MEAN_TOLERANCE = 10  # Average pixel difference tolerance


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS


def is_color_inverted(original_path: Path, inverted_path: Path) -> bool:
    """
    Returns True if inverted_path is roughly the color-inverted version of original_path
    """
    original = cv2.imread(str(original_path))
    inverted = cv2.imread(str(inverted_path))

    if original is None or inverted is None:
        raise ValueError(f"Cannot read images: {original_path}, {inverted_path}")

    # Resize inverted to match original if needed
    if original.shape != inverted.shape:
        inverted = cv2.resize(inverted, (original.shape[1], original.shape[0]))

    # Convert to float for calculation
    original = original.astype(np.float32)
    inverted = inverted.astype(np.float32)

    # Compute difference from perfect inversion
    diff = np.abs((inverted + original) - 255)
    mean_diff = diff.mean()

    return mean_diff <= MEAN_TOLERANCE


def find_inverted_file(stem: str) -> Path | None:
    for f in INVERTED_DIR.iterdir():
        if is_image_file(f) and f.stem == stem:
            return f
    return None


def main():
    if not INPUT_DIR.exists():
        print(f"❌ input_images folder not found: {INPUT_DIR}")
        return

    if not INVERTED_DIR.exists():
        print(f"❌ inverted folder not found: {INVERTED_DIR}")
        return

    images = [f for f in INPUT_DIR.iterdir() if is_image_file(f)]

    print("🎨 Color Inversion Verification\n")

    for img in images:
        try:
            inverted_file = find_inverted_file(img.stem)
            if inverted_file is None:
                print(f"{img.name} | ❌ inverted file not found")
                continue

            if is_color_inverted(img, inverted_file):
                print(f"{img.name} | SUCCESSFULLY INVERTED ✅")
            else:
                print(f"{img.name} | ❌ NOT INVERTED")

        except Exception as e:
            print(f"{img.name} | ❌ {e}")

    print("\n✅ Color inversion check finished")


if __name__ == "__main__":
    main()
