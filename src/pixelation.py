from pathlib import Path
import cv2


def pixelate_image(image_path: Path, out_path: Path, pixel_size: int = 16) -> None:
    """
    Pixelates an image by downscaling then upscaling with nearest-neighbor.
    pixel_size controls the blockiness (higher = bigger blocks).
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    h, w = img.shape[:2]
    pixel_size = max(1, int(pixel_size))

    # Compute downscaled size (smaller size => bigger pixel blocks)
    small_w = max(1, w // pixel_size)
    small_h = max(1, h // pixel_size)

    # Downscale then upscale using nearest neighbor
    small = cv2.resize(img, (small_w, small_h), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    ok = cv2.imwrite(str(out_path), pixelated)
    if not ok:
        raise RuntimeError(f"Failed to write output image: {out_path}")
