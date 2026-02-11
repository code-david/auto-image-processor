# auto-image-processor

Automated Image Processing using DevOps CI Pipeline

---

## Activity Overview

This laboratory activity involves designing and implementing an automated image processing application using Python and OpenCV. The system processes images automatically when they are added to a designated input directory.

To demonstrate DevOps workflow and automation, the application is integrated with GitHub Actions CI, ensuring that updates are validated automatically on every push.

---

Technologies Used

-Python 3

-OpenCV (opencv-python)

-GitHub & GitHub Actions

-PyTest

---

## Features

The system automatically applies the following image processing techniques:

- **Image Resizing** – Standardizes image dimensions for consistent processing.

- **Image Compression** – Reduces file size while maintaining acceptable quality.

- **Pixelation** – Creates a mosaic effect by reducing and reconstructing pixel resolution.

- **Color Inversion** – Produces a negative image effect by inverting pixel values.

- **Binary Conversion** – Converts images into black-and-white using thresholding.

All processed images are saved automatically to the output directory.

---

## Project Structure

```
auto-image-processor/
├── .github
│   └── workflows
│       └── ci.yml                     # CI workflow configuration
├── input_images                       # Raw input images
│   ├── sample1.png
│   ├── sample2.jpg
│   ├── sample3.jpg
│   ├── sample4.jpg
│   └── sample5.jpg
├── output_images                      # Processed image outputs
│   ├── binary/
│   ├── compressed/
│   ├── inverted/
│   ├── pixelated/
│   └── resized/
├── src                                # Core application source code
│   ├── __init__.py
│   ├── binary.py
│   ├── color_inversion.py
│   ├── image_compression.py
│   ├── pixelation.py
│   └── resizing.py
├── tests                              # Automated test scripts
│   ├── test_binary_output.py
│   ├── test_color_inversion_output.py
│   ├── test_compression_output.py
│   ├── test_pixelation_output.py
│   └── test_resizing_output.py
├── .gitignore
├── main.py
├── pytest.ini
├── README.md                          # Project documentation
└── requirements.txt                   # Project dependencies

```

---

## System Workflow

1. The system scans the `input_images/` directory for supported image files.

2. Detected images are loaded using OpenCV.

3. The defined image processing techniques are applied sequentially.

4. Processed images are saved automatically to the `output_images/` directory.

5. The CI pipeline runs on every push to validate the project.

---

## How to Run

```bash

git clone https://github.com/YOUR-USERNAME/auto-image-processor.git

cd auto-image-processor

pip install -r requirements.txt

python main.py
```
