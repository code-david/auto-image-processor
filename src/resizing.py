from pathlib import Path
import cv2


def resize_image(image_path: Path, out_path: Path, width: int = 100, height: int = 100) -> None:
    """
    Resizes an image to the exact width and height (in pixels).
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    width = max(1, int(width))
    height = max(1, int(height))

    resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    ok = cv2.imwrite(str(out_path), resized)
    if not ok:
        raise RuntimeError(f"Failed to write output image: {out_path}")
