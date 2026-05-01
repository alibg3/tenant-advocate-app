# Tenant & Housing Rights Advocate App

## Overview
This repository contains the **frontend application** for the Tenant & Housing Rights Advocate project. It provides an interactive interface where users can:

- Ask general tenancy questions  
- Upload lease agreements  
- Generate legal insights and communication drafts  

The application connects to a **FastAPI-based Agentic RAG backend**, which retrieves relevant legal information and generates grounded, explainable responses.

## Architecture

```text
User
↓
Streamlit App (this repo)
↓ HTTP request (streaming)
FastAPI Backend (tenant-advocate-rag repo)
↓
RAG Pipeline (LangChain + ChromaDB + OpenAI)
```

## Features
- Chat-based Q&A (general + lease-specific)
- Lease audit (full document analysis)
- Communication draft generation (tenant → landlord)
- Upload lease agreements (PDF)
- Session-based memory
- Streaming responses from backend

## Repository Structure
```bash
tenant-advocate-app/
│
├── app/                    # Streamlit application
│   ├── streamlit_app.py        # Main app entry point
│   ├── sidebar.py              # Lease upload + backend health status
│   ├── chat_tab.py             # Chat Q&A interface
│   ├── audit_tab.py            # Lease audit interface
│   ├── draft_tab.py            # Communication draft form
│   ├──session_state.py         # Central session state setup
│   └── ui_components.py
│
├── backend_client/         # Interface to FastAPI backend
│   ├── mock_backend.py         # For testing
│   └── api_client.py           # Calls FastAPI streaming endpoints
│
├── utils/                  # Helper functions 
│   ├── pdf_utils.py            # Extract text for /chat
│   └── response_utils.py       # Streaming display helper
│
├── assets/                 # Static assets (images, styles)
│
├── pyproject.toml          # Poetry configuration
├── poetry.lock
├── .env.example            # Environment variables template
└── README.md
```
## Setup

### 1. Clone the repository
```bash
git clone https://github.com/alibg3/tenant-advocate-app
cd tenant-advocate-app
```

### 2. Install dependencies (poetry)
```bash
poetry install
```
Active environment
```bash
poetry shell
```

## Environment Variables
Create a ```.env``` file:
```bash
FASTAPI_BASE_URL=https://your-render-api-url.onrender.com
USE_MOCK_BACKEND=false
```
NOTES
- ```USE_MOCK_BACKEND=true``` -> use mock responses (no backend)
- ```USE_MOCK_BACKEND=false``` -> connect to FastAPI backend

## Running App
```bash
poetry run streamlit run app/streamlit_app.py
```

## Backend Integration
The app communicates with the backend via streaming endpoints.

### Main Endpoints
- ```GET /health``` → backend status
- ```POST /chat``` → Q&A (JSON input, streaming output)
- ```POST /audit``` → lease audit (PDF upload, streaming output)
- ```POST /draft``` → communication draft (form + optional PDF, streaming output)

NOTES
- Responses are streamed token-by-token (Server-Sent Events), rather than returned as a single JSON object.
- API interactions are handled through the `api_client.py` module.
- The frontend does not directly perform HTTP requests; all communication is abstracted via the API client.


## Deployment
### Frontend
Hosted on Streamlit Community Cloud

### Backend
Hosted using FastAPI on Render