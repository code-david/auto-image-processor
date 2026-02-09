from pathlib import Path
import cv2

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

INPUT_DIR = Path(r"C:\Users\marmo\OneDrive\Documents\auto-image-processor\input_images")
OUTPUT_DIR = Path(r"C:\Users\marmo\OneDrive\Documents\auto-image-processor\output_images\compressed")

JPEG_QUALITY = 60


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS


def compress_image(input_path: Path, output_path: Path, quality: int = 60):
    image = cv2.imread(str(input_path))
    if image is None:
        raise ValueError(f"Cannot read image: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_file = output_path.with_suffix(".jpg")

    cv2.imwrite(
        str(output_file),
        image,
        [cv2.IMWRITE_JPEG_QUALITY, quality]
    )

    return output_file


def bytes_to_kb(size_bytes: int) -> float:
    return size_bytes / 1024


def main():
    if not INPUT_DIR.exists():
        print(f"❌ Input folder not found:\n{INPUT_DIR}")
        return

    images = [f for f in INPUT_DIR.iterdir() if is_image_file(f)]

    if not images:
        print("⚠️ No images found")
        return

    print("📦 Auto Image Compression Test\n")

    for img in images:
        try:
            original_size = img.stat().st_size

            output_file = compress_image(
                img,
                OUTPUT_DIR / img.stem,
                quality=JPEG_QUALITY
            )

            compressed_size = output_file.stat().st_size

            print(
                f"{img.name} | "
                f"{bytes_to_kb(original_size):.2f} KB → "
                f"{bytes_to_kb(compressed_size):.2f} KB"
            )

        except Exception as e:
            print(f"❌ {img.name}: {e}")

    print("\n✅ Compression test finished")


if __name__ == "__main__":
    main()
