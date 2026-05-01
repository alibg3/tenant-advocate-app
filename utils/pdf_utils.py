from io import BytesIO

import pdfplumber


def extract_pdf_text_from_bytes(pdf_bytes: bytes) -> str:
    """Extract plain text from PDF bytes for the Chat Q&A endpoint."""

    if not pdf_bytes:
        raise ValueError("No PDF content was provided.")

    try:
        text_parts = []

        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        extracted_text = "\n\n".join(text_parts).strip()

        if not extracted_text:
            raise ValueError(
                "Could not extract text from this PDF. Please use a text-based PDF, not a scanned image."
            )

        return extracted_text

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(f"PDF text extraction failed: {error}") from error


def validate_pdf_file(filename: str | None, file_size_bytes: int | None = None) -> None:
    """Validate uploaded PDF file name and size."""

    if not filename or not filename.lower().endswith(".pdf"):
        raise ValueError("Please upload a PDF file.")

    max_size_bytes = 10 * 1024 * 1024

    if file_size_bytes is not None and file_size_bytes > max_size_bytes:
        raise ValueError("File too large. Maximum size is 10MB.")