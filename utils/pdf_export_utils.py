from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def create_pdf_from_text(text: str, title: str = "Document") -> bytes:
    """Convert plain text/markdown-like content into simple PDF bytes."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 12))

    for line in text.splitlines():
        clean_line = line.strip()

        if not clean_line:
            story.append(Spacer(1, 8))
        else:
            story.append(Paragraph(clean_line, styles["BodyText"]))
            story.append(Spacer(1, 4))

    document.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes