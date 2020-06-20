# This module has helper functions to create a PDF of lecture slides with text captions as ouput.

from PyPDF2 import PdfFileMerger
from reportlab.pdfgen.canvas import Canvas


def create_pdf(filename, segments):
    
    # create a pdf slide the size of a letter in landscape
    canvas = Canvas(filename=filename, pagesize=(792.0, 612.0))
    canvas.save()