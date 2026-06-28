from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, courses, deadlines, sessions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StudySync API",
    description="Portfolio demonstration — coursework deadlines and study sessions with JWT auth and SQLite.",
    version="0.2.0",
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(deadlines.router)
app.include_router(sessions.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "studysync-api"}
