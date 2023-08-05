import cv2
import numpy as np
from PySide6.QtGui import QImage, QPixmap, qRgb


def mat_to_qpixmap(mat):
    if len(mat.shape) == 2:  # Grayscale image
        height, width = mat.shape
        bytes_per_line = width
        image_format = QImage.Format_Grayscale8
    elif len(mat.shape) == 3:  # RGB/BGR image
        height, width, _ = mat.shape
        bytes_per_line = 3 * width
        image_format = QImage.Format_RGB888
    else:
        raise ValueError("Unsupported image format")

    # Copy the data from the Mat to the QImage
    qimage = QImage(mat.data, width, height, bytes_per_line, image_format)

    # If the Mat uses BGR order, convert it to RGB before converting to QPixmap
    if len(mat.shape) == 3 and mat.shape[2] == 3:
        qimage = qimage.rgbSwapped()

    # Convert QImage to QPixmap
    qpixmap = QPixmap.fromImage(qimage)

    return qpixmap

# Example usage:
# if __name__ == "__main__":
#     # Load an image using OpenCV
#     image_path = "./data/lena.jpg"
#     mat = cv2.imread(image_path)

#     # Convert Mat to QPixmap
#     qpixmap = mat_to_qpixmap(mat)
    
 