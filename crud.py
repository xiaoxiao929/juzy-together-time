from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, date
from free_time.weekday import WeekdayStrategy
from free_time.weekend import WeekendStrategy


import models
import schemas

def get_users(db: Session):
    return db.query(models.User).all()

# =========================
# User
# =========================
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_status(db: Session, user_id: int, status: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    user.status = status
    db.commit()
    return user


# =========================
# Event
# =========================
# 在 crud.py 中新增這個衝突檢查函式
def check_event_conflict(db: Session, event: schemas.EventCreate):
    return db.query(models.Event).filter(
        models.Event.owner_id == event.owner_id,
        models.Event.start < event.end,  # 新行程的開始時間早於舊行程的結束時間
        models.Event.end > event.start    # 新行程的結束時間晚於舊行程的開始時間
    ).first()


def create_event(db: Session, event: schemas.EventCreate):
    # 行程衝突檢查
    conflict = db.query(models.Event).filter(
        models.Event.owner_id == event.owner_id,
        models.Event.start < event.end,
        models.Event.end > event.start
    ).first()

    if conflict:
        note = models.Notification(
            to_user_id=event.owner_id,
            message="⚠️ 行程與既有行程衝突"
        )
        db.add(note)
        db.commit()
        raise ValueError("行程時間衝突")

    db_event = models.Event(
        owner_id=event.owner_id,
        title=event.title,
        category=event.category,
        start=event.start,
        end=event.end,
        color=event.color
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events_by_users(db: Session, user_ids: list[int]):
    return db.query(models.Event).filter(
        models.Event.owner_id.in_(user_ids)
    ).all()


def search_events(
    db: Session,
    user_ids: list[int] | None,
    title: str | None,
    category: str | None,
    target_date: date | None
):
    q = db.query(models.Event)

    if user_ids:
        q = q.filter(models.Event.owner_id.in_(user_ids))

    if title:
        q = q.filter(models.Event.title.contains(title))

    if category:
        q = q.filter(models.Event.category == category)

    if target_date:
        day_start = datetime.combine(target_date, datetime.min.time())
        day_end = datetime.combine(target_date, datetime.max.time())
        q = q.filter(
            models.Event.start < day_end,
            models.Event.end > day_start
        )

    return q.all()



# =========================
# Free Time
# =========================
def find_free_times(db, user_ids, date_str, strategy):
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    day_start, day_end = strategy.get_day_range(target_date)

    events = db.query(models.Event).filter(
        models.Event.owner_id.in_(user_ids),
        models.Event.start < day_end,
        models.Event.end > day_start
    ).all()
    ...

    events = db.query(models.Event).filter(
        models.Event.owner_id.in_(user_ids),
        models.Event.start < day_end,
        models.Event.end > day_start
    ).all()

    busy = sorted([(e.start, e.end) for e in events])
    free = []
    cur = day_start

    for s, e in busy:
        if cur < s:
            free.append({"start": cur, "end": s})
        cur = max(cur, e)

    if cur < day_end:
        free.append({"start": cur, "end": day_end})

    return free



# =========================
# Invitation & Notification
# =========================
def create_invitation(db: Session, inv: schemas.InviteCreate):
    db_invitation = models.Invitation(
        event_id=inv.event_id,
        from_user=inv.from_user_id, # 👈 確保與 schemas 一致
        to_user_id=inv.to_user_id,  # 👈 確保與 schemas 一致
        status="pending"
    )
    db_note = models.Notification(
    to_user_id=inv.to_user_id,
        message=f"📩 你收到來自使用者 {inv.from_user_id} 的新邀請：{inv.message or ''}"
    )
    db.add(db_invitation)
    db.add(db_note)
    db.commit()
    db.refresh(db_invitation)
    return db_invitation



def get_notifications(db: Session, user_id: int):
    return db.query(models.Notification).filter(
        models.Notification.to_user_id == user_id
    ).order_by(models.Notification.created_at.desc()).all()


# =========================
# Work Hours
# =========================
def calculate_month_work_hours(db: Session, user_id: int):
    now = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0)

    events = db.query(models.Event).filter(
        models.Event.owner_id == user_id,
        models.Event.start >= month_start,
        models.Event.category == "打工"
    ).all()


    total_hours = 0.0
    for e in events:
        total_hours += (e.end - e.start).total_seconds() / 3600

    return round(total_hours, 2)
