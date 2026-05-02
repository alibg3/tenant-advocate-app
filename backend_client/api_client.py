import os
from collections.abc import Generator

import requests
import streamlit as st

from dotenv import load_dotenv

load_dotenv()


def get_api_base_url() -> str:
    api_base_url = os.getenv("FASTAPI_BASE_URL")

    if not api_base_url:
        try:
            api_base_url = st.secrets.get("FASTAPI_BASE_URL")
        except Exception:
            api_base_url = None

    if not api_base_url:
        raise RuntimeError("FASTAPI_BASE_URL is not configured.")

    return api_base_url.rstrip("/")


def check_backend_health() -> dict | None:
    try:
        response = requests.get(f"{get_api_base_url()}/health", timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


def _stream_sse_response(response: requests.Response) -> Generator[str, None, None]:
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue

        if line.startswith("data: "):
            token = line.replace("data: ", "", 1)

            if token == "[DONE]":
                break

            yield token.replace("\\n", "\n")


def stream_chat(question, lease_text=None, chat_history=None):
    payload = {
        "question": question,
        "lease_text": lease_text,
        "chat_history": chat_history or [],
    }

    response = requests.post(
        f"{get_api_base_url()}/chat",
        json=payload,
        stream=True,
        timeout=120,
    )

    response.raise_for_status()
    return _stream_sse_response(response)


def stream_audit(pdf_bytes, filename):
    files = {
        "file": (filename, pdf_bytes, "application/pdf"),
    }

    response = requests.post(
        f"{get_api_base_url()}/audit",
        files=files,
        stream=True,
        timeout=180,
    )

    response.raise_for_status()
    return _stream_sse_response(response)


def stream_draft(
    situation,
    tenant_name="",
    landlord_name="",
    pdf_bytes=None,
    filename=None,
):
    data = {
        "situation": situation,
        "tenant_name": tenant_name,
        "landlord_name": landlord_name,
    }

    files = None
    if pdf_bytes and filename:
        files = {
            "file": (filename, pdf_bytes, "application/pdf"),
        }

    response = requests.post(
        f"{get_api_base_url()}/draft",
        data=data,
        files=files,
        stream=True,
        timeout=180,
    )

    response.raise_for_status()
    return _stream_sse_response(response)