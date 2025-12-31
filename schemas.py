from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# 與 main.py 相容用（別名）


# ---------- User ----------
class UserCreate(BaseModel):
    name: str = Field(..., example="昭巧")

class UserOut(BaseModel):
    id: int
    name: str
    status: str

    class Config:
        from_attributes = True


class UserStatusUpdate(BaseModel):
    status: str = Field(..., example="忙碌")


# ---------- Event ----------
class EventBase(BaseModel):
    title: str
    category: str = "其他"
    start: datetime
    end: datetime
    color: str = "#cccccc"


class EventCreate(EventBase):
    owner_id: int


class EventOut(EventBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


# ---------- Invitation ----------
class InviteCreate(BaseModel):
    from_user_id: int
    to_user_id: int
    event_id: Optional[int] = None
    message: Optional[str] = None

class InviteOut(BaseModel):
    id: int
    from_user: int
    to_user_id: int
    event_id: Optional[int]
    #message: Optional[str]
    status: str
    #created_at: Optional[datetime] = None

    class Config:             # 👈 加上這三行
        from_attributes = True


# ---------- Notification ----------
class NotificationOut(BaseModel):
    id: int
    message: str
    #created_at: Optional[datetime] = None
    is_read: bool

    class Config:
        from_attributes = True


# ---------- Free Time ----------
class FreeTimeRequest(BaseModel):
    user_ids: List[int]
    date: str
