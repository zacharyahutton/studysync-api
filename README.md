# StudySync API

StudySync is a **portfolio demonstration** FastAPI backend for tracking university courses, assignment deadlines, and study sessions. It shows JWT authentication, Pydantic validation, SQLAlchemy ORM with SQLite, and auto-generated OpenAPI docs at `/docs`. This is a learning and reference implementation—not a production SaaS.

## Stack

- Python 3.11+
- FastAPI, Pydantic, SQLAlchemy 2.x, SQLite
- JWT (python-jose), bcrypt (passlib)
- Uvicorn, pytest, httpx

## Prerequisites

- Python 3.11 or newer
- `pip` and a virtual environment (recommended)

## Setup

```bash
git clone https://github.com/zacharyahutton/studysync-api.git
cd studysync-api
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

## How to run

```bash
uvicorn app.main:app --reload
```

- API base: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs

A local `studysync.db` SQLite file is created on first startup.

## How to test

### Automated tests

```bash
pytest -q
```

### Manual curl flow

Register:

```bash
curl -s -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"student@example.com\",\"password\":\"password123\"}"
```

Sample response:

```json
{"message":"User registered"}
```

Login (save the token):

```bash
curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"student@example.com\",\"password\":\"password123\"}"
```

Sample response:

```json
{"access_token":"<JWT>","token_type":"bearer"}
```

Create a course and deadline (replace `TOKEN`):

```bash
curl -s -X POST http://127.0.0.1:8000/courses \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Data Structures\",\"code\":\"CS201\"}"

curl -s -X POST http://127.0.0.1:8000/deadlines \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"course_id\":1,\"title\":\"Lab 3\",\"due\":\"2026-12-01T17:00:00Z\"}"
```

## API endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | Service health |
| POST | `/auth/register` | No | Register with email + password |
| POST | `/auth/login` | No | Login, returns JWT |
| GET | `/courses` | Bearer | List your courses |
| POST | `/courses` | Bearer | Create course |
| GET | `/courses/{id}` | Bearer | Get one course |
| DELETE | `/courses/{id}` | Bearer | Delete course |
| GET | `/deadlines` | Bearer | List your deadlines |
| POST | `/deadlines` | Bearer | Create deadline |
| PATCH | `/deadlines/{id}` | Bearer | Update deadline |
| DELETE | `/deadlines/{id}` | Bearer | Delete deadline |
| GET | `/study-sessions` | Bearer | List study sessions |
| POST | `/study-sessions` | Bearer | Log a session |
| DELETE | `/study-sessions/{id}` | Bearer | Delete session |

## Project structure

```
app/
  main.py           FastAPI app and router wiring
  config.py         JWT and database settings
  database.py       SQLAlchemy engine and session
  models.py         User, Course, Deadline, StudySession
  schemas.py        Pydantic request/response models
  auth_utils.py     Password hashing and JWT helpers
  deps.py           Current-user dependency
  routers/          Route modules (auth, courses, deadlines, sessions)
tests/
  test_api.py       pytest smoke tests
```

## Portfolio disclaimer

This repository supports the [StudySync case study](https://github.com/zacharyahutton/portfolio) on my portfolio site. It intentionally implements a **subset** of what a full product would need (no email verification, no Postgres deployment, no refresh tokens). The case study describes production-oriented patterns; this repo is the honest, runnable starter.

## Future improvements

- Alembic migrations and PostgreSQL connection string
- Refresh tokens and password reset
- Pagination and filtering on deadlines
- Per-user deadline reminders (background jobs)

## License

MIT
