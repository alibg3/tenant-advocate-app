import streamlit as st


def initialise_session_state():
    """Initialise all Streamlit session state variables used across the app."""

    defaults = {
        "messages": [],
        "chat_history": [],
        "lease_bytes": None,
        "lease_filename": None,
        "lease_text": None,
        "audit_result": "",
        "draft_result": "",
        "backend_status": None,
        "lease_uploader_key": 0,
        "upload_error": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value