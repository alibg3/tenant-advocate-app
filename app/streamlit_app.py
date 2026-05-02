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

st.markdown(
    """
    <style>
    div[data-testid="stFileUploaderDropzoneInstructions"] > div > span {
        display: none;
    }

    h1 {
        font-size: clamp(42px, 3.5vw, 58px) !important;
        white-space: nowrap;
        text-align: center;
    }

    .app-footer-landing {
        position: fixed;
        left: 18px;
        bottom: 12px;
        font-size: 12px;
        color: var(--text-color);
        opacity: 0.45;
        z-index: 9999;
        padding: 4px 6px;
        text-align: left;
        line-height: 1.45;
    }

    .app-footer-main {
        margin-top: 48px;
        padding: 16px 0 8px 0;
        font-size: 12px;
        color: var(--text-color);
        opacity: 0.55;
        text-align: right;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


initialise_session_state()

if "show_app" not in st.session_state:
    st.session_state.show_app = False


# ---------------- Landing page ----------------
if not st.session_state.show_app:
    st.markdown("<br>", unsafe_allow_html=True)

    # Title block
    title_left, title_centre, title_right = st.columns([0.2, 3, 0.2])
    with title_centre:
        st.title("Tenant & Housing Rights Advocate")

    # Description block
    desc_left, desc_centre, desc_right = st.columns([1, 2, 1])
    with desc_centre:
        st.markdown(
            """
This prototype helps tenants understand housing rights and prepare practical next steps.

- **Chat Q&A:** Ask general tenancy questions or questions about an uploaded lease.
- **Lease Audit:** Upload a lease and generate a risk-based review of key clauses.
- **Communication Draft:** Generate a draft message to a landlord, agent, or housing provider.
            """
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Button block
    btn_left, btn_centre, btn_right = st.columns([2, 1, 2])
    with btn_centre:
        if st.button("Start using the tool", type="primary", use_container_width=True):
            st.session_state.show_app = True
            st.rerun()

    st.markdown(
        """
        <div class="app-footer-landing">
            <div>General information only — not legal advice. Do not upload highly sensitive information. Uploaded lease data is processed temporarily during the active session and is not stored.</div>
            <div>Developed by Team 7 — Artificial Intelligence Principles and Applications (Autumn 2026) — UTS Master of Data Science and Innovation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


# ---------------- Main app ----------------
render_sidebar()

st.title("Tenant & Housing Rights Advocate")
st.caption("Chat, audit a lease, or generate a communication draft.")

if st.button("← Back to home"):
    st.session_state.show_app = False
    st.rerun()

chat_tab, audit_tab, draft_tab = st.tabs(
    ["Chat Q&A", "Lease Audit", "Communication Draft"]
)

with chat_tab:
    render_chat_tab()

with audit_tab:
    render_audit_tab()

with draft_tab:
    render_draft_tab()


st.markdown(
    """
    <div class="app-footer-main">
        <div>General information only — not legal advice.</div>
        <div>Developed by Team 7 — Artificial Intelligence Principles and Applications (Autumn 2026) — UTS Master of Data Science and Innovation</div>
    </div>
    """,
    unsafe_allow_html=True,
)