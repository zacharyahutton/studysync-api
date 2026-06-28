from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Message(BaseModel):
    message: str


class CourseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    code: str = Field(min_length=1, max_length=32)


class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str


class DeadlineCreate(BaseModel):
    course_id: int | None = None
    title: str = Field(min_length=1, max_length=200)
    due: datetime
    status: str = "pending"


class DeadlineUpdate(BaseModel):
    title: str | None = None
    due: datetime | None = None
    status: str | None = None
    course_id: int | None = None


class DeadlineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int | None
    title: str
    due: datetime
    status: str


class StudySessionCreate(BaseModel):
    course_id: int | None = None
    started_at: datetime
    duration_minutes: int = Field(ge=1, le=1440)
    notes: str | None = None


class StudySessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int | None
    started_at: datetime
    duration_minutes: int
    notes: str | None
