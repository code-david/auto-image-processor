from pathlib import Path
import cv2

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS


def compress_image(
    input_path: Path,
    output_path: Path,
    quality: int = 60,
):
    image = cv2.imread(str(input_path))
    if image is None:
        raise ValueError(f"Cannot read image: {input_path}")

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Always save as JPEG for compression
    output_file = output_path.with_suffix(".jpg")

    cv2.imwrite(
        str(output_file),
        image,
        [cv2.IMWRITE_JPEG_QUALITY, quality]
    )
