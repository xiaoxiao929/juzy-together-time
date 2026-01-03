# 揪是要你 🤝（Juzy Together Time）

一個多人行程管理與共同空閒時間查詢系統  
使用 **FastAPI + SQLAlchemy + SQLite + 原生 JavaScript** 實作



## 📌 專案功能

本專案實作以下功能：

1. 使用者自行新增行程（POST /events）
2. 查詢好友之間的行程（GET /events?user_ids=1,2）
3. 查詢多位使用者的共同空閒時間（POST /free-times）
4. 發出行程邀約（POST /invites）
5. 行程提醒功能（以 notifications 資料表模擬）（GET /notifications/{user_id}）
6. 使用者目前狀態設定（PUT /users/{user_id}/status）
7. 行程搜尋功能（GET /events/search）
8. 行程衝突檢查（新增行程時自動檢查並回傳 conflict=true）
9. 紀錄本月打工時數（GET /work-hours/{user_id}?year=2025&month=12）
10. 當有人邀請你時，於通知列表中顯示（invites → notifications）
11. 行程顏色標記（event.color）


## 🎯 設計模式（加分項目）

本專案於「共同空閒時間查詢」功能中導入  
**策略模式（Strategy Pattern）**

將不同日期情境（平日、假日）的空閒時間計算邏輯
封裝為獨立策略類別（WeekdayStrategy、WeekendStrategy），
提升系統擴充性與可維護性。



## 🚀 啟動方式

### 1️⃣ 安裝套件
```bash
pip install -r requirements.txt
