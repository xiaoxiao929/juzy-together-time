from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
from free_time.weekday import WeekdayStrategy
from free_time.weekend import WeekendStrategy


import models
import schemas
import crud
from database import SessionLocal, engine



# 建立資料表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="揪是要你",
    description="好友共同空檔揪團系統",
    version="1.0"
)

# ===== 資料庫 Dependency =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
       

# ===== 前端 =====
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=FileResponse)
def index():
    return FileResponse("static/index.html")

# =================================================
# 👤 使用者
# =================================================

@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.patch("/users/{user_id}/status", response_model=schemas.UserOut)
def update_status(user_id: int, status: schemas.UserStatusUpdate, db: Session = Depends(get_db)):
    user = crud.update_user_status(db, user_id, status.status)
    if not user:
        raise HTTPException(404, "User not found")
    return user

# =================================================
# 📅 行程
# =================================================

@app.post("/events", response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    conflict = crud.check_event_conflict(db, event)
    if conflict:
        raise HTTPException(400, "行程時間衝突")
    return crud.create_event(db, event)

@app.get("/events", response_model=List[schemas.EventOut])
def list_events(
    user_ids: str = "",
    title: str | None = None,
    category: str | None = None,
    date: date | None = None,
    db: Session = Depends(get_db)
):
    ids = [int(i) for i in user_ids.split(",") if i]
    return crud.search_events(db, ids, title, category, date)

# =================================================
# ⏰ 共同空檔
# =================================================

@app.post("/free-times")
def free_times(req: schemas.FreeTimeRequest, db: Session = Depends(get_db)):
    return crud.find_free_times(db, req.user_ids, req.date)

# =================================================
# 📩 邀約
# =================================================

@app.post("/invites", response_model=schemas.InviteOut)
def send_invite(inv: schemas.InviteCreate, db: Session = Depends(get_db)):
    return crud.create_invitation(db, inv)

@app.get("/notifications/{user_id}")
def get_notifications(user_id: int, db: Session = Depends(get_db)):
    return crud.get_notifications(db, user_id)

# =================================================
# ⏱️ 打工時數
# =================================================

@app.get("/work-hours/{user_id}")
def work_hours(user_id: int, db: Session = Depends(get_db)):
    return {
        "user_id": user_id,
        "hours": crud.calculate_month_work_hours(db, user_id)
    }


@app.post("/free-times")
def free_times(req: schemas.FreeTimeRequest, db: Session = Depends(get_db)):
    target_date = datetime.strptime(req.date, "%Y-%m-%d").date()

    if target_date.weekday() >= 5:
        strategy = WeekendStrategy()
    else:
        strategy = WeekdayStrategy()

    return crud.find_free_times(db, req.user_ids, req.date, strategy)

