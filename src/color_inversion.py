from pathlib import Path
import cv2


def invert_colors(image_path: Path, out_path: Path) -> None:
    """
    Inverts the colors of an image (negative).
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    inverted = cv2.bitwise_not(img)

    ok = cv2.imwrite(str(out_path), inverted)
    if not ok:
        raise RuntimeError(f"Failed to write output image: {out_path}")
