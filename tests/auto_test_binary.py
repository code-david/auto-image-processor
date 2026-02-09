from pathlib import Path
import cv2

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Path to the binary output folder
BINARY_DIR = Path(r"C:\Users\marmo\OneDrive\Documents\auto-image-processor\output_images\binary")


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS


def is_grayscale(image_path: Path) -> bool:
    """
    Returns True if the image is grayscale (black and white)
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")

    # If image has 2 dimensions → grayscale
    if len(img.shape) == 2:
        return True

    # If image has 3 channels, check if all channels are equal
    if len(img.shape) == 3 and img.shape[2] == 3:
        b, g, r = cv2.split(img)
        return (b == g).all() and (b == r).all()

    return False


def main():
    if not BINARY_DIR.exists():
        print(f"❌ Binary folder not found: {BINARY_DIR}")
        return

    images = [f for f in BINARY_DIR.iterdir() if is_image_file(f)]

    if not images:
        print("⚠️ No images found in binary folder")
        return

    print("🖤 Binary Image Verification\n")

    for img in images:
        try:
            if is_grayscale(img):
                print(f"{img.name} | DONE ✅")
            else:
                print(f"{img.name} | ❌ NOT BLACK AND WHITE")

        except Exception as e:
            print(f"{img.name} | ❌ {e}")

    print("\n✅ Binary check finished")


if __name__ == "__main__":
    main()
