from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Course, StudySession, User
from app.schemas import StudySessionCreate, StudySessionRead

router = APIRouter(prefix="/study-sessions", tags=["study-sessions"])


def _owned_course(db: Session, user_id: int, course_id: int | None) -> None:
    if course_id is None:
        return
    course = db.query(Course).filter(Course.id == course_id, Course.user_id == user_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@router.get("", response_model=list[StudySessionRead])
def list_sessions(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> list[StudySession]:
    return (
        db.query(StudySession)
        .filter(StudySession.user_id == user.id)
        .order_by(StudySession.started_at.desc())
        .all()
    )


@router.post("", response_model=StudySessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    body: StudySessionCreate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> StudySession:
    _owned_course(db, user.id, body.course_id)
    session = StudySession(user_id=user.id, **body.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    session = (
        db.query(StudySession)
        .filter(StudySession.id == session_id, StudySession.user_id == user.id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    db.delete(session)
    db.commit()
