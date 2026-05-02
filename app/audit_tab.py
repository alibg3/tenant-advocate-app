import streamlit as st

from backend_client.mock_backend import stream_audit
from utils.response_utils import render_stream
from utils.pdf_export_utils import create_pdf_from_text


def render_audit_tab() -> None:
    """Render Lease Audit tab."""

    st.subheader("Lease Audit")

    st.write(
        "Run a structured review of the uploaded lease against NSW tenancy law. "
        "The audit will identify standard, unfair, favourable, or potentially illegal clauses."
    )

    if not st.session_state.get("lease_bytes"):
        st.warning("Please upload a lease PDF in the sidebar before running an audit.")
        return

    st.success(f"Lease ready for audit: {st.session_state.lease_filename}")

    # ##DEBUG START: confirm raw PDF data available for /audit endpoint
    # with st.expander("DEBUG audit payload"):
    #     st.write("Endpoint: POST /audit")
    #     st.write("Input format: multipart/form-data")
    #     st.write("Lease input: raw PDF bytes")
    #     st.json(
    #         {
    #             "filename": st.session_state.get("lease_filename"),
    #             "pdf_bytes_available": st.session_state.get("lease_bytes") is not None,
    #             "pdf_bytes": len(st.session_state.get("lease_bytes") or b""),
    #             "pdf_size_mb": round(
    #                 len(st.session_state.get("lease_bytes") or b"") / (1024 * 1024),
    #                 2,
    #             ),
    #         }
    #     )
    # ##DEBUG END

    col1, col2, _ = st.columns([1, 1, 3])

    with col1:
        run_audit = st.button("Run Audit", key="run_audit_button", use_container_width=True)

    with col2:
        clear_audit = st.button(
            "Clear audit result",
            key="clear_audit_result_button",
            disabled=not bool(st.session_state.get("audit_result")),
            use_container_width=True,
        )

    if clear_audit:
        st.session_state.audit_result = ""
        st.rerun()

    ##if user clicks Run Audit then generate new result
    if run_audit:
        try:
            full_response = ""

            with st.spinner("Reviewing lease and generating audit report..."):
                stream = stream_audit(
                    pdf_bytes=st.session_state.lease_bytes,
                    filename=st.session_state.lease_filename,
                )

                for token in stream:
                    full_response += token

            st.session_state.audit_result = full_response
            st.rerun()

            # ##DEBUG START: confirm streamed response was captured
            # with st.expander("DEBUG audit response"):
            #     st.json(
            #         {
            #             "response_received": bool(full_response),
            #             "response_length": len(full_response),
            #             "stored_in_session_state": (
            #                 st.session_state.audit_result == full_response
            #             ),
            #         }
            #     )
            # ##DEBUG END

        except Exception as exc:
            st.error(
                "Could not complete the lease audit. Please try again later.\n\n"
                f"Error details: `{exc}`"
            )
            return

        # Show stored or newly generated audit result
    if st.session_state.get("audit_result") and not run_audit:
        st.divider()
        st.markdown("### Audit Result")
        st.markdown(st.session_state.audit_result)

        audit_pdf = create_pdf_from_text(
            st.session_state.audit_result,
            title="NSW Lease Audit Report",
            )

        st.download_button(
            label="Download audit as PDF",
            data=audit_pdf,
            file_name="lease_audit_report.pdf",
            mime="application/pdf",
            key="download_audit_pdf_button",
        )