import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
from backend_client.api_client import check_backend_health
from utils.pdf_utils import extract_pdf_text_from_bytes, validate_pdf_file


def render_sidebar() -> None:
    """Render sidebar with backend status, lease upload and reset controls."""

    with st.sidebar:
        st.header("Tenant Advocate")

        render_backend_status()
        st.divider()

        render_lease_upload()
        st.divider()

#### mocked backend version of render_backend_status
# def render_backend_status() -> None:
#     """Render backend status placeholder.

#     This will later call the FastAPI /health endpoint.
#     """

#     st.subheader("Backend Status")

#     if st.session_state.get("backend_status"):
#         st.success("Backend connected")
#     else:
#         st.warning("Mock mode / backend not connected")
#### finished mocked version

@st.cache_data(ttl=30)
def get_cached_backend_status():
    return check_backend_health()


def render_backend_status() -> None:
    st.subheader("Backend Status")

    status = get_cached_backend_status()
    st.session_state.backend_status = status

    if status and status.get("api_configured") and status.get("knowledge_base_ready"):
        st.success("Backend connected")
    elif status:
        st.warning("Backend reachable, but not fully ready")
    else:
        st.error("Backend not connected")


def render_lease_upload() -> None:
    """Render PDF upload and store lease bytes + extracted text in session state."""

    st.subheader("Lease Upload")

    uploaded_file = st.file_uploader(
        "Upload lease PDF",
        type=["pdf"],
        key=f"lease_uploader_{st.session_state.lease_uploader_key}",
        help=(
            "Optional. Upload a lease to ask document-specific questions, "
            "run a lease audit or generate a communication draft."
        ),
    )

    st.caption("Maximum file size: 10MB. Text-based PDFs only.")

    # IMPORTANT:
    # If uploaded_file is None, do not clear the lease.
    # The lease should only be cleared when the user clicks "Clear uploaded lease".
    if uploaded_file is not None:
        try:
            validate_pdf_file(
                filename=uploaded_file.name,
                file_size_bytes=uploaded_file.size,
            )

            lease_bytes = uploaded_file.read()
            lease_text = extract_pdf_text_from_bytes(lease_bytes)

            st.session_state.lease_bytes = lease_bytes
            st.session_state.lease_filename = uploaded_file.name
            st.session_state.lease_text = lease_text
            st.session_state.upload_error = None

        except ValueError as error:
            st.session_state.lease_bytes = None
            st.session_state.lease_filename = None
            st.session_state.lease_text = None
            st.session_state.upload_error = str(error)
            st.session_state.lease_uploader_key += 1
            st.rerun()

    if st.session_state.get("upload_error"):
        st.error(st.session_state.upload_error)

    if st.session_state.get("lease_bytes"):
        st.success("Lease uploaded successfully.")
        st.caption(f"File: {st.session_state.get('lease_filename')}")
    else:
        st.info("No lease uploaded. General questions are still available.")

    if st.session_state.get("lease_bytes"):
        if st.button("Clear uploaded lease"):
            st.session_state.lease_bytes = None
            st.session_state.lease_filename = None
            st.session_state.lease_text = None
            st.session_state.audit_result = ""
            st.session_state.draft_result = ""
            st.session_state.upload_error = None
            st.session_state.lease_uploader_key += 1
            st.rerun()