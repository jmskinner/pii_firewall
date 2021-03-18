from PIL import Image
from presidio_image_redactor import ImageRedactorEngine
from pdf2image import convert_from_path, convert_from_bytes
import os, psutil
import time
from urllib.request import urlopen
import memory_profiler

@profile
def main() :
    # images = convert_from_path('/Users/skinner/Desktop/mpcs/practicum/final_project/Jake Skinner Project 3 Results.pdf')
    data = urlopen('http://mensenhandel.nl/files/pdftest2.pdf').read()
    images = convert_from_bytes(data, 'rb')
    # Set up the engine, loads the NLP module (spaCy model by default)]
    engine = ImageRedactorEngine()

# Redact the image with pink color
    redacted_images = []
    for image in images:
        redacted_images.append(engine.redact(image, (255, 192, 203)))
    print(redacted_images)
    #
    # redacted_images.save('testing_pdf_redaction.pdf', "PDF" ,resolution=100.0, save_all=True, append_images=redacted_images)

if __name__ == '__main__':
    main()
