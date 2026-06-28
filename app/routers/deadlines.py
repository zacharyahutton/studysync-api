from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Course, Deadline, User
from app.schemas import DeadlineCreate, DeadlineRead, DeadlineUpdate

router = APIRouter(prefix="/deadlines", tags=["deadlines"])


def _owned_course(db: Session, user_id: int, course_id: int | None) -> None:
    if course_id is None:
        return
    course = db.query(Course).filter(Course.id == course_id, Course.user_id == user_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@router.get("", response_model=list[DeadlineRead])
def list_deadlines(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> list[Deadline]:
    return db.query(Deadline).filter(Deadline.user_id == user.id).order_by(Deadline.due).all()


@router.post("", response_model=DeadlineRead, status_code=status.HTTP_201_CREATED)
def create_deadline(
    body: DeadlineCreate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Deadline:
    _owned_course(db, user.id, body.course_id)
    deadline = Deadline(user_id=user.id, **body.model_dump())
    db.add(deadline)
    db.commit()
    db.refresh(deadline)
    return deadline


@router.patch("/{deadline_id}", response_model=DeadlineRead)
def update_deadline(
    deadline_id: int,
    body: DeadlineUpdate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Deadline:
    deadline = db.query(Deadline).filter(Deadline.id == deadline_id, Deadline.user_id == user.id).first()
    if not deadline:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deadline not found")
    data = body.model_dump(exclude_unset=True)
    if "course_id" in data:
        _owned_course(db, user.id, data["course_id"])
    for key, value in data.items():
        setattr(deadline, key, value)
    db.commit()
    db.refresh(deadline)
    return deadline


@router.delete("/{deadline_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deadline(
    deadline_id: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    deadline = db.query(Deadline).filter(Deadline.id == deadline_id, Deadline.user_id == user.id).first()
    if not deadline:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deadline not found")
    db.delete(deadline)
    db.commit()
