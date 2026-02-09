from pathlib import Path
import cv2

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS


def invert_colors(input_path: Path, output_path: Path) -> Path:
    img = cv2.imread(str(input_path))
    if img is None:
        raise ValueError(f"Cannot read image: {input_path}")

    inverted = cv2.bitwise_not(img)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), inverted):
        raise RuntimeError(f"Failed to write output: {output_path}")

    return output_path
