# Crop Care Crop — Backend

FastAPI backend for **Crop Care Crop**, an AI-powered crop disease detection
and recommendation system (college final-year project).

## Current status

| Feature | Status |
|---|---|
| FastAPI app skeleton, config, CORS, logging, error handling | ✅ Implemented |
| `GET /api/v1/health` | ✅ Implemented |
| Versioned router structure (`/api/v1`) | ✅ Implemented |
| Image-upload prediction endpoint (`POST /api/v1/predictions`) | ✅ Wired end-to-end; ML layer is a stub → returns `503` until the model is connected |
| Database (PostgreSQL) integration | ⏳ Plumbing ready (`app/database/`), models/endpoints in the DB task |
| Recommendation engine / risk analysis | ⏳ Route + service registered → returns `501` |
| AI chatbot (LangChain + Llama 3 / Ollama) | ⏳ Route + service registered → returns `501` |

**Nothing is faked:** no fake predictions, no fake DB calls. Everything that
is not built yet returns an explicit, documented HTTP error.

## Tech stack

- **Backend:** FastAPI, Pydantic v2, pydantic-settings, Uvicorn
- **Database (planned):** PostgreSQL, SQLAlchemy 2 (async), asyncpg
- **ML (planned):** PyTorch / YOLO / OpenCV / scikit-learn
- **LLM (planned):** LangChain, LangGraph, Llama 3 via Ollama
- **Frontend (separate repo):** React / Next.js

## Project structure
