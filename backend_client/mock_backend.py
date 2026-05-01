import re
import time
from collections.abc import Generator


def _mock_stream_response(text: str) -> Generator[str, None, None]:
    """Simulate token-by-token streaming while preserving Markdown spacing."""

    tokens = re.findall(r"\S+|\s+", text)

    for token in tokens:
        yield token
        time.sleep(0.01)


def stream_chat(
    question: str,
    lease_text: str | None = None,
    chat_history: list[list[str]] | None = None,
) -> Generator[str, None, None]:
    """Mock streaming chat response."""

    has_lease = lease_text is not None and lease_text.strip() != ""

    if has_lease:
        response = (
            "**Mock Chat Response**\n\n"
            "This question will be answered using NSW tenancy law and the uploaded lease. "
            "The final version will stream responses from the FastAPI backend.\n\n"
            "**Question received:** "
            f"{question}"
        )
    else:
        response = (
            "**Mock Chat Response**\n\n"
            "This is a general tenancy question. The final version will retrieve relevant "
            "NSW tenancy law context and stream a grounded answer from the FastAPI backend.\n\n"
            "**Question received:** "
            f"{question}"
        )

    return _mock_stream_response(response)


def stream_audit(
    pdf_bytes: bytes,
    filename: str,
) -> Generator[str, None, None]:
    """Mock streaming lease audit response."""

    response = (
        "**Mock NSW Lease Audit Report**\n\n"
        f"**Uploaded file:** {filename}\n\n"
        "This tab will send the raw PDF to the FastAPI `/audit` endpoint. "
        "The final response will include a risk summary, detailed findings, and overall assessment."
    )

    return _mock_stream_response(response)


def stream_draft(
    situation: str,
    tenant_name: str = "",
    landlord_name: str = "",
    pdf_bytes: bytes | None = None,
    filename: str | None = None,
) -> Generator[str, None, None]:
    """Mock streaming communication draft response."""

    tenant = tenant_name if tenant_name else "[YOUR NAME]"
    landlord = landlord_name if landlord_name else "[LANDLORD/AGENT NAME]"

    response = (
        "## Mock Communication Draft\n\n"
        "**DRAFT — Read carefully and personalise before sending**\n\n"
        f"To: {landlord}\n\n"
        f"Dear {landlord},\n\n"
        f"I am writing regarding the following issue: {situation}\n\n"
        "The final version will generate a more complete draft using NSW tenancy law context"
    )

    if pdf_bytes and filename:
        response += f" and the uploaded lease file: **{filename}**."

    response += f"\n\nRegards,\n{tenant}"

    return _mock_stream_response(response)