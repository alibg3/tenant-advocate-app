import streamlit as st

from backend_client.mock_backend import stream_audit
from utils.response_utils import render_stream


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

    ##DEBUG START: confirm raw PDF data available for /audit endpoint
    with st.expander("DEBUG audit payload"):
        st.write("Endpoint: POST /audit")
        st.write("Input format: multipart/form-data")
        st.write("Lease input: raw PDF bytes")
        st.json(
            {
                "filename": st.session_state.get("lease_filename"),
                "pdf_bytes_available": st.session_state.get("lease_bytes") is not None,
                "pdf_bytes": len(st.session_state.get("lease_bytes") or b""),
                "pdf_size_mb": round(
                    len(st.session_state.get("lease_bytes") or b"") / (1024 * 1024),
                    2,
                ),
            }
        )
    ##DEBUG END

    run_audit = st.button("Run Audit")

    ##if user clicks Run Audit then generate new result
    if run_audit:
        placeholder = st.empty()

        try:
            with st.spinner("Reviewing lease and generating audit report..."):
                stream = stream_audit(
                    pdf_bytes=st.session_state.lease_bytes,
                    filename=st.session_state.lease_filename,
                )

                full_response = render_stream(stream, placeholder)

            st.session_state.audit_result = full_response

            ##DEBUG START: confirm streamed response was captured
            with st.expander("DEBUG audit response"):
                st.json(
                    {
                        "response_received": bool(full_response),
                        "response_length": len(full_response),
                        "stored_in_session_state": (
                            st.session_state.audit_result == full_response
                        ),
                    }
                )
            ##DEBUG END

        except Exception as exc:
            st.error(
                "Could not complete the lease audit. Please try again later.\n\n"
                f"Error details: `{exc}`"
            )
            return

    #show stored result ONLY when not actively generating
    if st.session_state.get("audit_result") and not run_audit:
        st.divider()

        if st.session_state.get("audit_result"):
            if st.button("Clear audit result"):
                st.session_state.audit_result = ""
                st.rerun()

        st.markdown("### Latest Audit Result")
        st.markdown(st.session_state.audit_result)