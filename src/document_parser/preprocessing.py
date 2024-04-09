"""Script does a few preprocessing steps that will make work faster and easier:
- Extract PDF pages as images
- Extract text from images
"""

import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from IPython.display import display  # To display images in Jupyter notebook/Colab
from pathlib import Path
import re
from io import TextIOWrapper
from document_parser.embedding_manager import EmbeddingManager

_USE_GPU = cv2.cuda.getCudaEnabledDeviceCount() > 0
_FILE_NAME = "mercedes-c-klasse-cabriolet-2022-mai-a205-comand-betriebsanleitung-01.pdf"
_PDF_PATH = "/Users/tobiasgerlach/Documents/Code/document_parser/documents/"  # Replace with the path to your PDF
_BATCH_SIZE = 10
_FILEPATH = Path(__file__).parent
_EM_MANAGER = EmbeddingManager()


def process_batch(start, end):
    # Verarbeite Batch
    images = convert_from_path(
        _PDF_PATH + _FILE_NAME, first_page=start, last_page=end, dpi=200
    )

    # Extrahiere text mittels OCR
    for i, image in enumerate(images):
        greyscale_image = _convert_image_to_grayscale(image)
        text = pytesseract.image_to_string(greyscale_image)

        text_file_path = str(
            _FILEPATH / Path(_FILE_NAME[:-3] + f"_page_{start + i}.txt")
        )
        store_txt_object(text_file_path, text)

        image_file_path = str(
            _FILEPATH / Path(_FILE_NAME[:-3] + f"page_{start + i}.png")
        )
        store_image_object(path=image_file_path, image=image)

    # Clear the images list to free up memory
    del images


def store_txt_object(path, text):
    # Hier könnte ggfs eine Ablage in DB stattfidnen
    with open(path, "w") as file:
        file.write(text)
    # Qdrant is notwendig für anständige Vektorsuche


def store_image_object(path, image):
    image.save(image_file_path)


# Function to preprocess an image with OpenCV
def _convert_image_to_grayscale(image):
    image_cv = np.array(image)
    if _USE_GPU:
        # Upload image to GPU
        image_gpu = cv2.cuda_GpuMat(image_cv)
        # Convert to grayscale
        gray_gpu = cv2.cuda.cvtColor(image_gpu, cv2.COLOR_BGR2GRAY)
        # Download image from GPU to CPU
        image_cv = gray_gpu.download()
    else:
        # Convert to grayscale
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    return Image.fromarray(image_cv)


def get_chapters():
    """APPENDS to exesting chapter files. The files have the names of the chapters, minus special chars and whitespaces."""
    dir = Path(
        "/Users/tobiasgerlach/Documents/Code/document_parser/src/document_parser/batch_texts"
    )
    for pth in dir.iterdir():
        with open(pth) as file:
            line = file.readline()
            numbers = re.findall(r"\d+", line)
            if len(numbers) > 1 or len(numbers) == 0:
                print(
                    "Page skipped because it could either not be assiged to a chapter or a page. "
                    + "To avoid incongruencies, I removed it from chapterwise data. "
                    + "It is still stored in the pages database."
                )
                continue
            chapter = line.replace(numbers[0], "").strip()
            chapter = "".join(e for e in chapter if e.isalnum())

            # print(numbers)
            print(f"Chapter: {chapter}")
            _append_to_chapter(chapter=chapter, file=file)


def _append_to_chapter(chapter: str, file: TextIOWrapper):
    chapter_dir = "/Users/tobiasgerlach/Documents/Code/document_parser/src/document_parser/batch_chapters"
    chapter_dir = Path(chapter_dir)
    chapter_filepath = chapter_dir / Path(chapter + ".txt")
    with open(chapter_filepath, mode="a") as chapter_file:
        chapter_file.writelines(file.readlines())


def extract_information_from_pdf():
    # Aufteilung in batches um RAM Fehler zu vermeiden
    total_pages = 700  # Maximale Anzahl Seiten
    batches = (total_pages + _BATCH_SIZE - 1) // _BATCH_SIZE

    for batch in range(batches):
        start_page = batch * _BATCH_SIZE + 1
        end_page = min(start_page + _BATCH_SIZE - 1, total_pages)
        process_batch(start_page, end_page, batch)


def main():
    """Main programm of the preprocessing step"""
    extract_information_from_pdf()


if __name__ == "__main__":
    # main()
    # get_chapters()
    pass
