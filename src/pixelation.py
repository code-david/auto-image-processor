from pathlib import Path
import cv2

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS


def pixelate_image(input_path: Path, output_path: Path, pixel_size: int = 16) -> Path:
    img = cv2.imread(str(input_path))
    if img is None:
        raise ValueError(f"Cannot read image: {input_path}")

    h, w = img.shape[:2]
    pixel_size = max(1, int(pixel_size))

    small_w = max(1, w // pixel_size)
    small_h = max(1, h // pixel_size)

    small = cv2.resize(img, (small_w, small_h), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), pixelated):
        raise RuntimeError(f"Failed to write output: {output_path}")

    return output_path
