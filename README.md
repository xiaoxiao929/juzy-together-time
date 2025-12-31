揪是要你 - FastAPI 範例專案
----------------------------------
內容：
- 完整 FastAPI 後端，使用 SQLAlchemy + SQLite 儲存資料 (database.db)
- 簡單前端 (static/index.html, static/app.js, static/styles.css) 與後端互動
- 自動產生 Swagger UI / ReDoc：啟動後訪問 http://127.0.0.1:8000/docs 或 /redoc
- 已實作功能對應您要求的 11 項：
  1. 使用者自行輸入行程 (POST /events)
  2. 查詢好友之間的行程 (GET /events?user_ids=1,2)
  3. 查詢共同空閒時間 (POST /free-times)
  4. 發出邀約 (POST /invites)
  5. 行程提醒功能（以 notifications 資料表模擬）(GET /notifications/{user_id})
  6. 使用者目前狀態 (PUT /users/{user_id}/status)
  7. 行程搜尋功能 (GET /events/search)
  8. 行程衝突檢查 (自動於新增時檢查並回傳 conflict=true)
  9. 紀錄本月打工時數 (GET /work-hours/{user_id}?year=2025&month=12)
  10. 當有人邀你 → 在通知列表中顯示 (invites -> notifications)
  11. 行程顏色標記 (event.color)
啟動：
1. 安裝依賴：pip install -r requirements.txt
2. 啟動服務：uvicorn main:app --reload
3. 打開瀏覽器：http://127.0.0.1:8000
