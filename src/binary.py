from pathlib import Path
import cv2

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS


def to_binary(input_path: Path, output_path: Path, threshold: int = 128) -> Path:
    img = cv2.imread(str(input_path))
    if img is None:
        raise ValueError(f"Cannot read image: {input_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold = max(0, min(255, int(threshold)))
    _, bw = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), bw):
        raise RuntimeError(f"Failed to write output: {output_path}")

    return output_path
