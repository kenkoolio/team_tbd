# This module has helper functions to create a PDF of lecture slides with text captions as ouput.

import os
import shutil
import textwrap
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
    try:
        # size of a letter in portrait
        WIDTH = 612.0
        HEIGHT = 792.0

        TEXT_X = 72
        TEXT_Y = (HEIGHT / 2)

        # create temp directory for slides
        TEMP_SLIDE_FOLDER='./tempslides'

        if not os.path.exists(TEMP_SLIDE_FOLDER):
            os.mkdir(TEMP_SLIDE_FOLDER)

        # make a temp slide for each segment
        for i, segment in enumerate(segments):
            temp_pdf_slide_path = filename+'-slide-'+str(i)+'.pdf'
            temp_pdf_slide_path = os.path.join(TEMP_SLIDE_FOLDER, temp_pdf_slide_path)
            
            # create a pdf slide 
            canvas = Canvas(filename=temp_pdf_slide_path, pagesize=(WIDTH, HEIGHT))

            # insert the image into the canvas
            canvas.drawImage(
                segment.imagePath,                      # image source
                (WIDTH*.1),                             # x-coord, with 10% left margin (origin starts from bottom left)
                ((HEIGHT/2)-(HEIGHT*.1)),               # y-coord, halfway up, with 10% top margin
                width=(WIDTH-(WIDTH*.2)),               # width of image is page width minus 20% (for 10% margins on each side)
                height=(HEIGHT/2),                      # height of image is half of page height
                preserveAspectRatio=True,               # keep aspect ratio
                anchor='n'                              # anchor the image to the top (north) of containing box
                )

            # insert text into the canvas
            write_text(canvas, segment.text, TEXT_X, TEXT_Y)
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
    
    except Exception as e:
        print(f"Exception in 'create_pdf': {e}")
        raise


def write_text(canvas, text, x, y):
    FONT = "Helvetica"
    FONT_SIZE = 16
    LEADING = None          #default leading of None is 1.2 x font size in reportlab

    transcription_text = wrap_transcription(text)

    canvas.setFont(FONT, FONT_SIZE, LEADING)
    
    # pull y coordinate up one line before the loop starts
    y+=FONT_SIZE

    for line in transcription_text:
        y-=FONT_SIZE
        canvas.drawString(x, y, line)


def wrap_transcription(input_str):
    WRAP_WIDTH = 45

    if len(input_str) > WRAP_WIDTH:
        return textwrap.wrap(input_str, width=WRAP_WIDTH)
    else:
        return [input_str]
