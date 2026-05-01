import streamlit as st
from collections.abc import Generator


def render_stream(
    stream_generator: Generator[str, None, None],
    placeholder: st.delta_generator.DeltaGenerator,
) -> str:
    """Render a streaming response token by token."""

    full_response = ""

    for token in stream_generator:
        full_response += token
        placeholder.markdown(full_response + "▌")

    placeholder.markdown(full_response)
    return full_response