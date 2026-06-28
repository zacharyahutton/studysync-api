from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field

SECRET_KEY = "portfolio-demo-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

app = FastAPI(
    title="StudySync API",
    description="Portfolio demonstration — coursework deadline tracker starter",
    version="0.1.0",
)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Deadline(BaseModel):
    id: int
    course: str
    title: str
    due: datetime
    status: str = "pending"


class DeadlineCreate(BaseModel):
    course: str
    title: str
    due: datetime


# In-memory demo store — replace with SQLAlchemy in a full implementation
_users: dict[str, str] = {}
_deadlines: list[Deadline] = []
_next_id = 1


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": subject, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> str:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return email
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "studysync-api"}


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(body: UserCreate) -> dict[str, str]:
    if body.email in _users:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    _users[body.email] = pwd_context.hash(body.password)
    return {"message": "User registered"}


@app.post("/auth/login", response_model=Token)
def login(body: UserCreate) -> Token:
    hashed = _users.get(body.email)
    if not hashed or not pwd_context.verify(body.password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return Token(access_token=create_access_token(body.email))


@app.get("/deadlines", response_model=list[Deadline])
def list_deadlines(_user: Annotated[str, Depends(get_current_user)]) -> list[Deadline]:
    return _deadlines


@app.post("/deadlines", response_model=Deadline, status_code=status.HTTP_201_CREATED)
def create_deadline(
    body: DeadlineCreate,
    _user: Annotated[str, Depends(get_current_user)],
) -> Deadline:
    global _next_id
    deadline = Deadline(id=_next_id, **body.model_dump())
    _next_id += 1
    _deadlines.append(deadline)
    return deadline
