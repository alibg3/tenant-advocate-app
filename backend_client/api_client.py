
##-------------------- for now, we will use a mock backend that simulates streaming responses --------------------##
def stream_chat(question, lease_text=None, chat_history=None):
    raise NotImplementedError("FastAPI chat endpoint is not connected yet.")


def stream_audit(pdf_bytes, filename):
    raise NotImplementedError("FastAPI audit endpoint is not connected yet.")


def stream_draft(situation, tenant_name="", landlord_name="", pdf_bytes=None, filename=None):
    raise NotImplementedError("FastAPI draft endpoint is not connected yet.")