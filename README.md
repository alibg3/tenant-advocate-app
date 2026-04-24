# Tenant & Housing Rights Advocate App

## Overview
This repository contains the **frontend application** for the Tenant & Housing Rights Advocate project. It provides an interactive interface where users can upload lease agreements and ask questions in plain English to better understand their tenancy rights.

The application connects to a **FastAPI-based Agentic RAG backend**, which retrieves relevant legal information and generates grounded, explainable responses.

## Architecture

```text
User
↓
Streamlit App (this repo)
↓ HTTP request
FastAPI Backend (tenant-advocate-rag repo)
↓
RAG Pipeline (LangChain + ChromaDB + OpenAI)
```

## Features
- Chat-based interface for questions
- Upload lease agreements (PDF)
- Session-based conversation memory

## Repository Structure
```bash
tenant-advocate-app/
│
├── app/                    # Streamlit application
│   ├── streamlit_app.py
│   ├── ui_components.py
│   └── session_state.py
│
├── backend_client/         # Interface to FastAPI backend
│   ├── mock_backend.py
│   └── api_client.py
│
├── utils/                  # Helper functions 
│   └── pdf_utils.py
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
git clone 
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
The app communicates with the backend using a simple API contract.

### Request
```

```
### Response
```

```

## Deployment
### Frontend
Hosted on Streamlit Community Cloud

### Backend
Hosted using FastAPI on Render