import streamlit as st


st.set_page_config(
    page_title="Tenant & Housing Rights Advocate",
    layout="wide"
)



##-----------------Session state setup-------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "lease_uploaded" not in st.session_state:
    st.session_state.lease_uploaded = False

if "lease_file_name" not in st.session_state:
    st.session_state.lease_file_name = None



###--------------------------Header-------------
st.title("Tenant & Housing Rights Advocate")
st.write(
    "Upload your lease agreement and ask questions about your tenancy rights in plain English."
)

st.info(
    "This is an early frontend prototype. Responses are currently mock answers until the FastAPI backend is connected. LET'S GOOOO!"
)



##------------------Sidebar lease upload-----------------------------
with st.sidebar:
    st.header("Lease Upload")

    uploaded_file = st.file_uploader(
        "Upload your lease agreement",
        type=["pdf"],
        help="Upload a PDF lease agreement and start asking questions."
    )

    if uploaded_file is not None:
        st.session_state.lease_uploaded = True
        st.session_state.lease_file_name = uploaded_file.name

        st.success("Lease uploaded successfully.")
        st.write(f"**File:** {uploaded_file.name}")

    else:
        st.warning("No lease uploaded yet.")

    st.divider()

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()



###-------------------status---------------------------

if st.session_state.lease_uploaded:
    st.success(f"Current lease: {st.session_state.lease_file_name}")
else:
    st.info("You can ask general tenancy questions now, or upload a lease for document-specific questions.")


###-------------------Chat history display---------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


###-------------------Chat input---------------------------
user_question = st.chat_input("Ask a question about your lease or tenancy rights...")

if user_question:
    st.session_state.messages.append(
        {"role": "user", "content": user_question}
    )

    with st.chat_message("user"):
        st.write(user_question)

if st.session_state.lease_uploaded:
    assistant_response = (
        "This is a mock response. In the final version, this question will be sent "
        "to the FastAPI backend. "
        "In the meantime, I can tell you a joke: "
        "How do you make an octopus laugh? "
        "With ten-tickles!"
    )
else:
    assistant_response = (
        "This is a mock response. In the final version, this question will be sent "
        "to the FastAPI backend. "
        "In the meantime, I can tell you a joke: "
        "Why did the tenant bring a ladder to the inspection? "
        "Because the rent was too high."

    )

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )

    with st.chat_message("assistant"):
        st.write(assistant_response)