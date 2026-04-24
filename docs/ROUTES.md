# 🛣️ 讀書筆記本系統 — 路由設計文件（ROUTES）

**版本**：v1.0  
**建立日期**：2026-04-25  
**作者**：Alice  
**狀態**：草稿  

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 首頁（書籍清單） | GET | `/` | `books/list.html` | 顯示所有書籍卡片，支援排序 |
| 書籍清單 | GET | `/books` | `books/list.html` | 同首頁，支援 sort_by 參數 |
| 新增書籍頁面 | GET | `/books/create` | `books/create.html` | 顯示空白新增表單 |
| 建立書籍 | POST | `/books/create` | — | 接收表單，寫入 DB，重導向詳細頁 |
| 書籍詳細頁 | GET | `/books/<int:id>` | `books/detail.html` | 顯示單筆完整資料 |
| 編輯書籍頁面 | GET | `/books/<int:id>/edit` | `books/edit.html` | 表單預填原始資料 |
| 更新書籍 | POST | `/books/<int:id>/edit` | — | 接收表單，更新 DB，重導向詳細頁 |
| 刪除書籍 | POST | `/books/<int:id>/delete` | — | 刪除書籍，重導向清單頁 |
| 搜尋頁面 | GET | `/search` | `search/index.html` | 顯示搜尋介面與初始結果 |
| 搜尋 API | GET | `/search/api` | — | 回傳 JSON，供即時搜尋使用 |
| 統計儀表板 | GET | `/dashboard` | `dashboard/index.html` | 顯示統計數字與圖表 |
| 金句收藏庫 | GET | `/quotes` | `quotes/index.html` | 顯示所有金句卡片 |
| 隨機金句 API | GET | `/quotes/random` | — | 回傳 JSON，一則隨機金句 |
| 標籤管理頁 | GET | `/tags` | `tags/index.html` | 列出所有標籤，可操作 |
| 新增標籤 | POST | `/tags/create` | — | 建立新標籤，重導向標籤頁 |
| 重新命名標籤 | POST | `/tags/<int:id>/edit` | — | 更新標籤名稱，重導向標籤頁 |
| 刪除標籤 | POST | `/tags/<int:id>/delete` | — | 刪除標籤，重導向標籤頁 |
| 匯出 CSV | GET | `/export/csv` | — | 下載所有書籍資料（CSV 格式） |
| 匯出 JSON | GET | `/export/json` | — | 下載所有書籍資料（JSON 格式） |

---

## 2. 路由詳細說明

### 📚 書籍模組（books.py）

---

#### `GET /` 與 `GET /books` — 書籍清單

- **輸入**：Query 參數 `sort_by`（`created_at` / `finished_at` / `rating` / `title`）、`order`（`asc` / `desc`）
- **處理邏輯**：呼叫 `Book.get_all(sort_by, order)`
- **輸出**：渲染 `books/list.html`，傳入 `books` 列表
- **錯誤處理**：若排序參數不合法則使用預設值

---

#### `GET /books/create` — 新增書籍頁面

- **輸入**：無
- **處理邏輯**：查詢 `Tag.get_all()` 取得所有標籤供下拉選單使用
- **輸出**：渲染 `books/create.html`，傳入 `tags` 列表
- **錯誤處理**：無特殊錯誤

---

#### `POST /books/create` — 建立書籍

- **輸入**：表單欄位 `title`、`author`、`finished_at`、`rating`、`review`、`cover_url`、`is_recommend`、`quote`、`page_count`、`tag_ids[]`
- **處理邏輯**：
  1. 驗證必填欄位（`title`、`author`、`finished_at`、`rating`、`review`）
  2. 呼叫 `Book.create(**data)`
  3. Flash 成功訊息
- **輸出**：`302 redirect` → `GET /books/<new_id>`
- **錯誤處理**：驗證失敗時重新渲染 `create.html` 並顯示錯誤訊息

---

#### `GET /books/<int:id>` — 書籍詳細頁

- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `Book.get_by_id(id)`
- **輸出**：渲染 `books/detail.html`，傳入 `book` 物件
- **錯誤處理**：書籍不存在時回傳 `404`

---

#### `GET /books/<int:id>/edit` — 編輯書籍頁面

- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `Book.get_by_id(id)`、`Tag.get_all()`
- **輸出**：渲染 `books/edit.html`，傳入 `book`（含原始資料）與 `tags` 列表
- **錯誤處理**：書籍不存在時回傳 `404`

---

#### `POST /books/<int:id>/edit` — 更新書籍

- **輸入**：URL 參數 `id`；表單欄位同新增表單
- **處理邏輯**：
  1. 取得書籍（不存在則 404）
  2. 驗證必填欄位
  3. 呼叫 `book.update(**data)`
  4. Flash 成功訊息
- **輸出**：`302 redirect` → `GET /books/<id>`
- **錯誤處理**：驗證失敗重新渲染 `edit.html`

---

#### `POST /books/<int:id>/delete` — 刪除書籍

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 取得書籍（不存在則 404）
  2. 呼叫 `book.delete()`
  3. Flash 成功訊息
- **輸出**：`302 redirect` → `GET /books`
- **錯誤處理**：書籍不存在時回傳 `404`

---

### 🔍 搜尋模組（search.py）

---

#### `GET /search` — 搜尋頁面

- **輸入**：Query 參數 `q`（關鍵字，選填）
- **處理邏輯**：若有 `q` 則呼叫 `Book.search(keyword=q)` 取得初始結果；查詢 `Tag.get_all()`
- **輸出**：渲染 `search/index.html`，傳入 `books`（初始結果）、`tags`、`q`
- **錯誤處理**：無結果時傳入空列表，模板顯示空狀態提示

---

#### `GET /search/api` — 搜尋 API（JSON）

- **輸入**：Query 參數 `q`、`category_ids`、`rating_min`、`rating_max`、`date_from`、`date_to`、`is_recommend`
- **處理邏輯**：呼叫 `Book.search(**params)`
- **輸出**：`application/json`，書籍列表（含高亮用的原始關鍵字）
- **錯誤處理**：參數不合法時回傳 `400 Bad Request`

---

### 📊 統計儀表板（dashboard.py）

---

#### `GET /dashboard` — 統計儀表板

- **輸入**：Query 參數 `period`（`year` / `all`，預設 `year`）
- **處理邏輯**：
  - 呼叫 `Book.count_all()`、`Book.count_by_year()`、`Book.count_by_month()`
  - 呼叫 `Book.average_rating()`、`Book.top_rated(3)`
  - 統計各標籤書籍數量（圓餅圖）、每月閱讀趨勢（折線圖）
- **輸出**：渲染 `dashboard/index.html`，傳入統計數據 dict
- **錯誤處理**：無資料時顯示零值，不拋出錯誤

---

### 💬 金句收藏（quotes.py）

---

#### `GET /quotes` — 金句收藏庫

- **輸入**：無
- **處理邏輯**：呼叫 `Book.get_with_quotes()`
- **輸出**：渲染 `quotes/index.html`，傳入 `books`（含金句的書籍）
- **錯誤處理**：無金句時模板顯示空狀態提示

---

#### `GET /quotes/random` — 隨機金句 API（JSON）

- **輸入**：無
- **處理邏輯**：呼叫 `Book.get_with_quotes()`，`random.choice()` 取一筆
- **輸出**：`application/json`，`{ quote, title, author }`
- **錯誤處理**：無金句時回傳 `404`

---

### 🏷️ 標籤管理（tags.py）

---

#### `GET /tags` — 標籤管理頁

- **輸入**：無
- **處理邏輯**：呼叫 `Tag.get_all()`，各標籤同時查詢書籍數量
- **輸出**：渲染 `tags/index.html`，傳入 `tags`（含書籍數量）
- **錯誤處理**：無

---

#### `POST /tags/create` — 新增標籤

- **輸入**：表單欄位 `name`
- **處理邏輯**：呼叫 `Tag.create(name)`，名稱重複時顯示錯誤
- **輸出**：`302 redirect` → `GET /tags`
- **錯誤處理**：名稱重複回傳錯誤訊息，不新增

---

#### `POST /tags/<int:id>/edit` — 重新命名標籤

- **輸入**：URL 參數 `id`；表單欄位 `name`
- **處理邏輯**：呼叫 `tag.update(name)`
- **輸出**：`302 redirect` → `GET /tags`
- **錯誤處理**：標籤不存在 `404`；名稱重複回傳錯誤

---

#### `POST /tags/<int:id>/delete` — 刪除標籤

- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `tag.delete()`（關聯的 `book_tags` 自動刪除）
- **輸出**：`302 redirect` → `GET /tags`
- **錯誤處理**：標籤不存在回傳 `404`

---

### 📥 資料匯出（export.py）

---

#### `GET /export/csv` — 匯出 CSV

- **輸入**：無
- **處理邏輯**：呼叫 `Book.export_all()`，產生 CSV 字串，帶入今日日期的檔名
- **輸出**：`Content-Disposition: attachment; filename=reading_notes_YYYYMMDD.csv`
- **錯誤處理**：無資料時仍回傳含標題列的空 CSV

---

#### `GET /export/json` — 匯出 JSON

- **輸入**：無
- **處理邏輯**：呼叫 `Book.export_all()`，序列化為 JSON
- **輸出**：`Content-Disposition: attachment; filename=reading_notes_YYYYMMDD.json`
- **錯誤處理**：無資料時回傳空陣列 JSON

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承自 | 說明 |
|----------|--------|------|
| `base.html` | — | 共用基礎版型（側邊欄、CSS、JS 載入） |
| `books/list.html` | `base.html` | 書籍清單卡片頁 |
| `books/create.html` | `base.html` | 新增書籍表單頁 |
| `books/detail.html` | `base.html` | 書籍詳細資料頁 |
| `books/edit.html` | `base.html` | 編輯書籍表單頁（預填資料） |
| `search/index.html` | `base.html` | 搜尋與篩選頁 |
| `dashboard/index.html` | `base.html` | 統計儀表板（含 Chart.js 圖表） |
| `quotes/index.html` | `base.html` | 金句收藏庫頁 |
| `tags/index.html` | `base.html` | 標籤管理頁 |

---

*本文件為 v1.0 草稿，如有修改請更新版本號與日期。*
