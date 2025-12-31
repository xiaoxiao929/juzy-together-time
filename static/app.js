// ================== 共用設定 ==================
const API_BASE = "http://127.0.0.1:8000";

const $ = (id) => document.getElementById(id);

function show(targetId, html) {
  const box = $(targetId);
  box.innerHTML = html;
}

// ================== 👤 建立使用者 ==================
async function createUser() {
  const name = $("user-name").value.trim();
  if (!name) {
    alert("⚠️ 請輸入名字");
    return;
  }

  const res = await fetch(`${API_BASE}/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  });

  const data = await res.json();

  show("user-created", `
    <h3>🎉 使用者建立成功</h3>
    <p>你的使用者 ID：<b>${data.id}</b></p>
    <p>你的名字：<b>${data.name}</b></p>
    <p>目前狀態：<b>${data.status}</b></p>
  `);
}

// ================== 🔄 更新狀態 ==================
async function updateStatus() {
  const userId = $("status-user-id").value;
  const status = $("user-status").value;

  if (!userId) {
    alert("⚠️ 請輸入使用者 ID");
    return;
  }

  const res = await fetch(`${API_BASE}/users/${userId}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status })
  });

  const data = await res.json();

  show("status-result", `
    <h3>🔄 狀態更新成功</h3>
    <p>使用者：${data.name}</p>
    <p>目前狀態：<b>${data.status}</b></p>
  `);
}

// ================== 📅 新增行程 ==================
async function createMyEvent() {
  const payload = {
    owner_id: Number($("ev-owner").value),
    title: $("ev-title").value,
    category: $("ev-category").value,
    start: $("ev-start").value,
    end: $("ev-end").value,
    color: $("ev-color").value || "#4f46e5"
  };

  if (!payload.owner_id || !payload.title || !payload.start || !payload.end) {
    alert("⚠️ 行程資料請填完整");
    return;
  }

  const res = await fetch(`${API_BASE}/events`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (res.status === 409) {
    alert("⛔ 行程時間衝突，請調整時間");
    return;
  }

  const data = await res.json();

  show("ev-created", `
    <h3>📅 行程新增成功</h3>
    <p><b>${data.title}</b>（${data.category}）</p>
    <p>🕒 ${data.start} ～ ${data.end}</p>
  `);
}

// ================== 🔍 行程搜尋 ==================
async function searchEvents() {
  const params = new URLSearchParams({
    user_ids: $("search-user-ids").value,
    title: $("search-title").value,
    category: $("search-category").value,
    date: $("search-date").value
  });

  const res = await fetch(`${API_BASE}/events?${params}`);

  if (!res.ok) {
    show("events-list", "⛔ 查詢失敗");
    return;
  }

  const data = await res.json();

  if (data.length === 0) {
    show("events-list", "📭 沒有符合條件的行程");
    return;
  }

  let html = "<h3>📋 行程列表</h3><ul>";
  data.forEach(e => {
    html += `<li>${e.title}（${e.start} ～ ${e.end}）</li>`;
  });
  html += "</ul>";

  show("events-list", html);
}

// ================== 🤝 查詢共同空閒時間 ==================
async function freeTime() {
  const userIdsInput = $("ft-ids");
  const dateInput = $("ft-date");
  const resultDiv = $("ft-result");

  if (!userIdsInput || !dateInput || !resultDiv) {
    alert("❌ 找不到查詢欄位或結果顯示區塊");
    return;
  }

  const userIds = userIdsInput.value;
  const date = dateInput.value;

  if (!userIds || !date) {
    alert("⚠️ 請輸入使用者 ID 與日期");
    return;
  }

  // 轉成陣列
  const idsArray = userIds.split(",").map(s => Number(s.trim()));

  const res = await fetch(`${API_BASE}/free-times`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_ids: idsArray, date })
  });

  if (!res.ok) {
    show("ft-result", "⛔ 查詢失敗");
    return;
  }

  const data = await res.json();

  if (data.length === 0) {
    show("ft-result", "📭 沒有共同空閒時間");
    return;
  }

  let html = "<h3>🤝 共同空閒時間</h3><ul>";
  data.forEach(t => {
    html += `<li>${t.start} ～ ${t.end}</li>`;
  });
  html += "</ul>";

  show("ft-result", html);
}




// ================== 📩 發送邀約 ==================
async function sendInvite() {
  const payload = {
    from_user_id: Number($("inv-from").value),
    to_user_id: Number($("inv-to").value),
    message: $("inv-msg").value
  };

  if (!payload.from_user_id || !payload.to_user_id) {
    alert("⚠️ 邀請者與被邀請者必填");
    return;
  }

  const res = await fetch(`${API_BASE}/invites`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  show("inv-result", "📨 邀約已送出！");
}

// ================== 🔔 通知 ==================
async function getNotifications() {
  const userId = $("not-user").value;
  if (!userId) {
    alert("⚠️ 請輸入使用者 ID");
    return;
  }

  const res = await fetch(`${API_BASE}/notifications/${userId}`);
  const data = await res.json();

  if (data.length === 0) {
    show("not-list", "📭 沒有任何通知");
    return;
  }

  let html = "<h3>🔔 通知列表</h3><ul>";
  data.forEach(n => {
    html += `<li>${n.message}</li>`;
  });
  html += "</ul>";

  show("not-list", html);
}

// ================== ⏱️ 打工時數 ==================
async function getWorkHours() {
  const userId = $("work-user").value;
  if (!userId) {
    alert("請輸入使用者 ID");
    return;
  }

  const res = await fetch(`${API_BASE}/work-hours/${userId}`);
  const data = await res.json();   // ✅ data 在這裡宣告

  console.log(data);               // ✅ 只能在 function 裡用

  const hours = data.hours ?? 0;

  $("work-result").innerHTML = `
    <h3>⏱️ 本月打工時數</h3>
    <p>${hours} 小時</p>
  `;
}

