import streamlit as st

##from backend_client.mock_backend import stream_draft #mock backend
from backend_client.api_client import stream_draft


MAX_SITUATION_LENGTH = 2000
MIN_SITUATION_LENGTH = 10


def render_draft_tab() -> None:
    """Render Communication Draft tab."""

    st.subheader("Communication Draft")

    st.write(
        "Generate a draft message to your landlord or agent based on your situation. "
        "You can optionally use the uploaded lease for cross-referencing."
    )

    if st.session_state.get("lease_bytes"):
        st.success(f"Optional lease context available: {st.session_state.lease_filename}")
    else:
        st.info("No lease uploaded. You can still generate a general draft.")

    form_key = st.session_state.draft_form_key

    situation = st.text_area(
        "Describe your situation",
        placeholder=(
            "Example: My hot water system has not worked for three days and "
            "my landlord has not responded to my repair request."
        ),
        height=160,
        max_chars=MAX_SITUATION_LENGTH,
        key=f"draft_situation_{form_key}",
    )

    tenant_name = st.text_input(
        "Tenant name (optional)",
        placeholder="Leave blank to use [YOUR NAME]",
        key=f"tenant_name_{form_key}",
    )

    landlord_name = st.text_input(
        "Landlord or agent name (optional)",
        placeholder="Leave blank to use [LANDLORD/AGENT NAME]",
        key=f"landlord_name_{form_key}",
    )

    col1, col2, col3, _ = st.columns([1, 1, 1, 3])

    with col1:
        generate_draft = st.button("Generate draft", key="generate_draft_button", use_container_width=True)

    with col2:
        clear_form = st.button("Clear form", key="clear_draft_form_button", use_container_width=True)

    with col3:
        clear_draft = st.button(
            "Clear result",
            key="clear_draft_result_button",
            disabled=not bool(st.session_state.get("draft_result")),
            use_container_width=True,
        )

    if clear_form:
        st.session_state.draft_form_key += 1
        st.rerun()

    if clear_draft:
        st.session_state.draft_result = ""
        st.rerun()

    # # DEBUG START: confirm /draft payload
    # with st.expander("DEBUG draft payload"):
    #     st.write("Endpoint: POST /draft")
    #     st.write("Input format: multipart/form-data")
    #     st.json(
    #         {
    #             "situation": situation,
    #             "situation_length": len(situation.strip()) if situation else 0,
    #             "tenant_name": tenant_name,
    #             "landlord_name": landlord_name,
    #             "pdf_bytes_available": st.session_state.get("lease_bytes") is not None,
    #             "filename": st.session_state.get("lease_filename"),
    #             "pdf_size_bytes": len(st.session_state.get("lease_bytes") or b""),
    #         }
    #     )
    # # DEBUG END

    if generate_draft:
        situation = situation.strip()

        if len(situation) < MIN_SITUATION_LENGTH:
            st.error("Please describe your situation in at least 10 characters.")
            return

        if len(situation) > MAX_SITUATION_LENGTH:
            st.error("Situation is too long. Please keep it under 2,000 characters.")
            return

        try:
            full_response = ""

            with st.spinner("Generating communication draft..."):
                stream = stream_draft(
                    situation=situation,
                    tenant_name=tenant_name.strip(),
                    landlord_name=landlord_name.strip(),
                    pdf_bytes=st.session_state.get("lease_bytes"),
                    filename=st.session_state.get("lease_filename"),
                )

                for token in stream:
                    full_response += token

            st.session_state.draft_result = full_response
            st.rerun()

        except Exception as exc:
            st.error(
                "Could not generate the communication draft. Please try again later.\n\n"
                f"Error details: `{exc}`"
            )
            return

    if st.session_state.get("draft_result"):
        st.divider()
        st.markdown("### Draft Result")
        st.markdown(st.session_state.draft_result)

        col1, col2, _ = st.columns([1, 1, 4])

        with col1:
            st.download_button(
                label="Download TXT",
                data=st.session_state.draft_result,
                file_name="communication_draft.txt",
                mime="text/plain",
                key="download_draft_txt_button",
                use_container_width=True,
            )

        with col2:
            st.download_button(
                label="Download MD",
                data=st.session_state.draft_result,
                file_name="communication_draft.md",
                mime="text/markdown",
                key="download_draft_md_button",
                use_container_width=True,
            )