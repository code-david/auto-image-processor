from pathlib import Path
import cv2


def to_binary(image_path: Path, out_path: Path, threshold: int = 128) -> None:
    """
    Converts an image to black and white using a threshold.
    """
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    threshold = max(0, min(255, int(threshold)))

    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    ok = cv2.imwrite(str(out_path), binary)
    if not ok:
        raise RuntimeError(f"Failed to write output image: {out_path}")
