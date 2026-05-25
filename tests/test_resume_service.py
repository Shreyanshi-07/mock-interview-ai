"""Tests for resume service."""

from io import BytesIO

from reportlab.pdfgen import canvas

from app.services.resume_service import extract_text_from_pdf


def create_test_pdf(text: str) -> BytesIO:
    """Create a simple PDF for testing."""

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 750, text)

    pdf.save()

    buffer.seek(0)

    return buffer


def test_extract_text_from_valid_pdf():
    """Test extraction from valid PDF."""

    test_text = "Software Engineer with Python skills"

    pdf_buffer = create_test_pdf(test_text)

    result = extract_text_from_pdf(pdf_buffer)

    assert isinstance(result, str)

    assert len(result) > 0


def test_extract_text_handles_empty_pdf():
    """Test extraction from empty PDF."""

    pdf_buffer = create_test_pdf("")

    result = extract_text_from_pdf(pdf_buffer)

    assert isinstance(result, str)

def test_extract_text_returns_string():
    """Ensure function always returns string."""

    pdf_buffer = create_test_pdf("Hello")

    result = extract_text_from_pdf(pdf_buffer)

    assert type(result) is str