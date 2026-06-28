# StudySync API

> **Portfolio demonstration** — a starter FastAPI backend for tracking coursework deadlines and study sessions. This is a learning/reference implementation, not a production SaaS product.

## Problem

Practice secure REST API patterns: JWT authentication, Pydantic validation, SQLAlchemy ORM, and auto-generated OpenAPI docs.

## Stack

- Python 3.11+
- FastAPI · Pydantic · SQLAlchemy · SQLite · JWT · bcrypt · Uvicorn

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Endpoints (starter)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/auth/register` | Register user (demo) |
| POST | `/auth/login` | Login, returns JWT |
| GET | `/deadlines` | List deadlines (auth required) |

## Disclaimer

This repository exists to support my [portfolio case study](https://github.com/zacharyahutton/portfolio). Code is intentionally scoped for demonstration and coursework-style learning.

## License

MIT
