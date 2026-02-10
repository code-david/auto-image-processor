from pathlib import Path
import cv2


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_image_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTS


def compress_image(image_path: Path, out_path: Path, quality: int = 60) -> None:
    """
    Compresses an image by saving as JPEG with the given quality (0-100).
    Note: Some JPEGs may become larger depending on the original encoder.
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Ensure quality range
    quality = max(0, min(100, int(quality)))

    # Write JPEG
    ok = cv2.imwrite(str(out_path), img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise RuntimeError(f"Failed to write output image: {out_path}")

    # Warn if output becomes larger
    original_size = image_path.stat().st_size
    compressed_size = out_path.stat().st_size
    if compressed_size > original_size:
        print(
            f"⚠️ Warning: {image_path.name} became larger after compression "
            f"({original_size} → {compressed_size} bytes)"
        )
