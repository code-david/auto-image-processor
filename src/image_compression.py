import cv2
from pathlib import Path


def is_image_file(path: Path) -> bool:
    return path.suffix.lower() in [".jpg", ".jpeg", ".png"]


def compress_image(image_path: Path, out_path: Path, quality: int = 60):
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Failed to read image: {image_path.name}")
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Write compressed image
    cv2.imwrite(
        str(out_path),
        image,
        [cv2.IMWRITE_JPEG_QUALITY, quality]
    )

    # ✅ ADD YOUR CODE RIGHT HERE
    original_size = image_path.stat().st_size
    compressed_size = out_path.stat().st_size

    if compressed_size > original_size:
        print(
            f"⚠️ Warning: {image_path.name} became larger after compression "
            f"({original_size} → {compressed_size} bytes)"
        )
