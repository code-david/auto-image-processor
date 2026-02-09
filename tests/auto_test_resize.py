from pathlib import Path
import cv2

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Paths
INPUT_DIR = Path(r"C:\Users\marmo\OneDrive\Documents\auto-image-processor\input_images")
OUTPUT_DIR = Path(r"C:\Users\marmo\OneDrive\Documents\auto-image-processor\output_images\resized")

EXPECTED_WIDTH = 100
EXPECTED_HEIGHT = 100


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS


def get_image_size(path: Path):
    img = cv2.imread(str(path))
    if img is None:
        raise ValueError(f"Cannot read image: {path}")
    h, w = img.shape[:2]
    return w, h


def find_resized_file(stem: str) -> Path | None:
    """
    Find a file in OUTPUT_DIR matching the stem of the input image.
    Handles possible extension changes.
    """
    for f in OUTPUT_DIR.iterdir():
        if is_image_file(f) and f.stem == stem:
            return f
    return None


def main():
    if not INPUT_DIR.exists():
        print("❌ input_images folder not found")
        return

    if not OUTPUT_DIR.exists():
        print("❌ resized output folder not found")
        return

    images = [f for f in INPUT_DIR.iterdir() if is_image_file(f)]

    if not images:
        print("⚠️ No images found in input_images")
        return

    print("📐 Resize Verification (100x100)\n")

    for img in images:
        try:
            before_w, before_h = get_image_size(img)

            resized_file = find_resized_file(img.stem)
            if resized_file is None:
                print(f"{img.name} | ❌ resized file not found")
                continue

            after_w, after_h = get_image_size(resized_file)

            if after_w == EXPECTED_WIDTH and after_h == EXPECTED_HEIGHT:
                print(
                    f"{img.name} | {before_w}x{before_h} → {after_w}x{after_h} | DONE ✅"
                )
            else:
                print(
                    f"{img.name} | {before_w}x{before_h} → {after_w}x{after_h} | ❌ WRONG SIZE"
                )

        except Exception as e:
            print(f"{img.name} | ❌ {e}")

    print("\n✅ Resize check finished")


if __name__ == "__main__":
    main()
