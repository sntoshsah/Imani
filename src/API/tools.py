import os
from PyPDF2 import PdfReader, PdfWriter
import cv2
import numpy as np
from pdf2image import convert_from_path

class ImageEditor:
    def __init__(self, image_path):
        """
        Initialize the ImageEditor with an image.

        :param image_path: Path to the image file
        """
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise FileNotFoundError(f"Image not found at {image_path}")
        self.edited_image = self.image.copy()

    def resize(self, width=None, height=None):
        """
        Resize the image while maintaining aspect ratio if only one dimension is provided.

        :param width: Desired width (optional)
        :param height: Desired height (optional)
        """
        h, w = self.edited_image.shape[:2]
        if width is None and height is None:
            raise ValueError("Either width or height must be provided.")
        if width is None:
            aspect_ratio = height / float(h)
            width = int(w * aspect_ratio)
        elif height is None:
            aspect_ratio = width / float(w)
            height = int(h * aspect_ratio)
        self.edited_image = cv2.resize(self.edited_image, (width, height))

    def rotate(self, angle):
        """
        Rotate the image by a specific angle.

        :param angle: Angle in degrees (positive values for counterclockwise)
        """
        h, w = self.edited_image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.edited_image = cv2.warpAffine(self.edited_image, rotation_matrix, (w, h))

    def apply_filter(self, filter_type):
        """
        Apply a filter to the image.

        :param filter_type: Type of filter ('blur', 'gaussian', 'median', 'edge')
        """
        if filter_type == 'blur':
            self.edited_image = cv2.blur(self.edited_image, (5, 5))
        elif filter_type == 'gaussian':
            self.edited_image = cv2.GaussianBlur(self.edited_image, (5, 5), 0)
        elif filter_type == 'median':
            self.edited_image = cv2.medianBlur(self.edited_image, 5)
        elif filter_type == 'edge':
            self.edited_image = cv2.Canny(self.edited_image, 100, 200)
        else:
            raise ValueError("Unsupported filter type. Choose from 'blur', 'gaussian', 'median', 'edge'.")

    def save_image(self, output_path):
        """
        Save the edited image to a file.

        :param output_path: Path to save the edited image
        """
        cv2.imwrite(output_path, self.edited_image)

    def reset(self):
        """
        Reset the edited image to the original.
        """
        self.edited_image = self.image.copy()

    def show_image(self, window_name='Image'):
        """
        Display the image in a window.

        :param window_name: Name of the window
        """
        cv2.imshow(window_name, self.edited_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

class PDFEditor:
    def __init__(self, pdf_path):
        """
        Initialize the PDFEditor with a PDF file.

        :param pdf_path: Path to the PDF file
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")
        self.pdf_path = pdf_path

    def convert_to_images(self, output_folder):
        """
        Convert PDF pages to images.

        :param output_folder: Folder to save the images
        :return: List of image file paths
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        images = convert_from_path(self.pdf_path)
        image_paths = []
        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
            image.save(image_path, "JPEG")
            image_paths.append(image_path)

        return image_paths

    def split_pdf(self, output_folder):
        """
        Split PDF into individual pages.

        :param output_folder: Folder to save the split PDF pages
        :return: List of split PDF file paths
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        reader = PdfReader(self.pdf_path)
        pdf_paths = []
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            pdf_path = os.path.join(output_folder, f"page_{i + 1}.pdf")
            with open(pdf_path, "wb") as output_pdf:
                writer.write(output_pdf)
            pdf_paths.append(pdf_path)

        return pdf_paths


    @staticmethod
    def merge_pdfs(pdf_paths, output_path):
        """
        Merge multiple PDF files into one.

        :param pdf_paths: List of PDF file paths to merge
        :param output_path: Path to save the merged PDF
        """
        writer = PdfWriter()
        for pdf_path in pdf_paths:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF not found at {pdf_path}")

            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)

        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

    def extract_text(self):
        """
        Extract text from the PDF.

        :return: Extracted text as a string
        """
        reader = PdfReader(self.pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text


if __name__ == "__main__":
    

# Example usage:
    editor = ImageEditor('path/to/image.jpg')
    editor.resize(width=500)
    editor.rotate(angle=45)
    editor.apply_filter('edge')
    editor.save_image('path/to/output.jpg')
