import streamlit as st

from backend_client.mock_backend import stream_chat
from utils.response_utils import render_stream


MAX_QUESTION_LENGTH = 2000
MAX_CHAT_HISTORY_TURNS = 4


def format_chat_history() -> list[list[str]]:
    """Format chat history as required by the API: [[question, answer], ...]."""

    return st.session_state.chat_history[-MAX_CHAT_HISTORY_TURNS:]


def render_chat_tab() -> None:
    """Render Chat Q&A tab."""

    st.subheader("Chat Q&A")

    st.write(
        "Ask general NSW tenancy questions, or upload a lease in the sidebar "
        "for document-specific questions."
    )

    if st.session_state.get("lease_text"):
        st.success("Lease context available for this chat.")
    else:
        st.info("No lease uploaded. General tenancy questions are still supported.")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

    # #display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about tenancy rights or your lease...")

    if not question:
        return

    question = question.strip()

    if not question:
        st.warning("Please enter a question before submitting.")
        return

    if len(question) > MAX_QUESTION_LENGTH:
        st.error("Question is too long. Please keep it under 2,000 characters.")
        return

    ##display and store user message
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    #stream assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()

        try:
            #### DEBUG START: show the payload being sent to the backend for this question
            debug_payload = {
                "question": question,
                "lease_text_preview": (
                    st.session_state.lease_text[:1000]
                    if st.session_state.get("lease_text")
                    else None
                ),
                "lease_text_length": (
                    len(st.session_state.lease_text)
                    if st.session_state.get("lease_text")
                    else 0
                ),
                "chat_history": format_chat_history(),
            }

            with st.expander("DEBUG API payload"):
                st.json(debug_payload)
            #### DEBUG END

            stream = stream_chat(
                question=question,
                lease_text=st.session_state.get("lease_text"),
                chat_history=format_chat_history(),
            )

            ###st.write("DEBUG chat_history:", format_chat_history()) ### debug
            full_response = render_stream(stream, placeholder)

        except Exception as exc:
            full_response = (
                "Could not reach the backend. Please try again later.\n\n"
                f"Error details: `{exc}`"
            )
            placeholder.error(full_response)

    ###store assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

    ###store API-compatible chat history as [question, answer] pairs
    st.session_state.chat_history.append(
        [question, full_response]
    )

    st.session_state.chat_history = st.session_state.chat_history[
        -MAX_CHAT_HISTORY_TURNS:
    ]