from pathlib import Path
import cv2

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS


def resize_image(input_path: Path, output_path: Path, width: int = 640, height: int = 480) -> Path:
    img = cv2.imread(str(input_path))
    if img is None:
        raise ValueError(f"Cannot read image: {input_path}")

    width = max(1, int(width))
    height = max(1, int(height))

    resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), resized):
        raise RuntimeError(f"Failed to write output: {output_path}")

    return output_path
