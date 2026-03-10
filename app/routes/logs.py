from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.database import get_db
from app.models.log import Log
from app.services.auth_service import decode_access_token

router = APIRouter(prefix="/logs", tags=["Logs"])
security = HTTPBearer(auto_error=False)


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    if credentials is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return int(payload["sub"])


class CreateLogRequest(BaseModel):
    title: str
    description: Optional[str] = None
    language: Optional[str] = None
    duration_minutes: Optional[int] = None
    mood: Optional[str] = None
    tags: Optional[str] = None

class UpdateLogRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    duration_minutes: Optional[int] = None
    mood: Optional[str] = None
    tags: Optional[str] = None

class LogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    language: Optional[str]
    duration_minutes: Optional[int]
    mood: Optional[str]
    tags: Optional[str]


@router.post("/", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
def create_log(body: CreateLogRequest, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    log = Log(user_id=user_id, **body.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/", response_model=list[LogResponse])
def get_logs(page: int = 1, limit: int = 10, language: Optional[str] = None, mood: Optional[str] = None, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    query = db.query(Log).filter(Log.user_id == user_id)
    if language:
        query = query.filter(Log.language.ilike(f"%{language}%"))
    if mood:
        query = query.filter(Log.mood.ilike(f"%{mood}%"))
    offset = (page - 1) * limit
    logs = query.order_by(Log.created_at.desc()).offset(offset).limit(limit).all()
    return logs


@router.get("/{log_id}", response_model=LogResponse)
def get_log(log_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    log = db.query(Log).filter(Log.id == log_id, Log.user_id == user_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log


@router.patch("/{log_id}", response_model=LogResponse)
def update_log(log_id: int, body: UpdateLogRequest, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    log = db.query(Log).filter(Log.id == log_id, Log.user_id == user_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(log, field, value)
    db.commit()
    db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(log_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    log = db.query(Log).filter(Log.id == log_id, Log.user_id == user_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log)
    db.commit()
    return