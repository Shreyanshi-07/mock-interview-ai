from typing import BinaryIO

import fitz


def extract_text_from_pdf(
    pdf_file: BinaryIO
) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_file: Uploaded PDF file object
        
    Returns:
        Extracted text content as a string
    """

    text = ""

    pdf_document = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    for page in pdf_document:

        text += page.get_text()

    return text