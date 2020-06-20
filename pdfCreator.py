# This module has helper functions to create a PDF of lecture slides with text captions as ouput.

import os
import shutil
from PyPDF2 import PdfFileMerger
from reportlab.pdfgen.canvas import Canvas


def create_pdf(filename, segments, output_dir):
    '''
    Creates pdf file from parsed video segments with text transcription
    Args: 
        filename <str>: name of the file
        segments <List[Segment]>: array of parsed input video segments and text
        output_dir <str>: directory to save generated .pdf
    Returns:
        output_pdf_name <str>: location of generated .pdf file
    '''
    # size of a letter in landscape
    WIDTH = 792.0
    HEIGHT = 612.0

    # create temp directory for slides
    TEMP_SLIDE_FOLDER='./tempslides'

    if not os.path.exists(TEMP_SLIDE_FOLDER):
        os.mkdir(TEMP_SLIDE_FOLDER)

    # make a temp slide for each segment
    for i, segment in enumerate(segments):
        temp_pdf_slide_path = filename+'-slide-'+i+'.pdf'
        temp_pdf_slide_path = os.path.join(TEMP_SLIDE_FOLDER, temp_pdf_slide_path)
        # create a pdf slide 
        canvas = Canvas(filename=temp_pdf_slide_path, pagesize=(WIDTH, HEIGHT))
        # insert the image into the canvas
        canvas.drawImage(segment.imagePath, 0, 0, preserveAspectRatio=True)
        # insert text into the canvas
        canvas.drawString(72, 72, segment.text)
        canvas.save()

    # combine temp slides into output
    pdf_merger = PdfFileMerger()
    for file in os.listdir(TEMP_SLIDE_FOLDER):
        pdf_merger.append(os.path.join(TEMP_SLIDE_FOLDER, file))

    # write to pdf
    output_pdf_name = os.path.join(output_dir, filename+'.pdf')
    with open(output_pdf_name, 'wb') as output_file:
        pdf_merger.write(output_file)

    # delete temp slide directory
    shutil.rmtree(TEMP_SLIDE_FOLDER)

    return output_pdf_name
