import streamlit as st

from session_state import initialise_session_state
from sidebar import render_sidebar
from chat_tab import render_chat_tab
from audit_tab import render_audit_tab
from draft_tab import render_draft_tab


st.set_page_config(
    page_title="Tenant & Housing Rights Advocate",
    page_icon="🏠",
    layout="wide",
)

##-------------hide default Streamlit file uploader instructions to avoid confusion with our custom uploader
st.markdown(
    """
    <style>
    div[data-testid="stFileUploaderDropzoneInstructions"] > div > span {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


initialise_session_state()

st.title("Tenant & Housing Rights Advocate")
st.write(
    "Ask general tenancy questions, upload a lease for document-specific support, "
    "run a lease audit or generate a communication draft."
)

st.info(
    "This is an early frontend prototype. Responses are currently mock answers until the FastAPI backend is connected."
)

render_sidebar()

chat_tab, audit_tab, draft_tab = st.tabs(
    ["Chat Q&A", "Lease Audit", "Communication Draft"]
)

with chat_tab:
    render_chat_tab()

with audit_tab:
    render_audit_tab()

with draft_tab:
    render_draft_tab()