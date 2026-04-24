# 🗺️ 讀書筆記本系統 — 流程圖文件（FLOWCHART）

**版本**：v1.0  
**建立日期**：2026-04-25  
**作者**：Alice  
**狀態**：草稿  

---

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
    Start([🌐 使用者開啟網站]) --> Home[📚 書籍清單頁\n首頁]

    Home --> Action{要執行什麼操作？}

    %% 新增書籍
    Action -->|新增筆記| Create[📝 新增書籍表單頁]
    Create --> FillForm[填寫書名、作者\n評分、心得等欄位]
    FillForm --> Validate{必填欄位\n是否完整？}
    Validate -->|否| ShowError[❌ 顯示錯誤提示]
    ShowError --> FillForm
    Validate -->|是| SaveBook[💾 儲存書籍]
    SaveBook --> Detail[📖 書籍詳細頁\n+ Toast 成功通知]

    %% 查看詳細頁
    Action -->|點擊書籍卡片| Detail
    Detail --> DetailAction{詳細頁操作}
    DetailAction -->|編輯| Edit[✏️ 編輯表單頁\n預填原始資料]
    Edit --> SaveEdit[💾 儲存變更]
    SaveEdit --> Detail
    DetailAction -->|刪除| ConfirmDelete{⚠️ 確認刪除？}
    ConfirmDelete -->|取消| Detail
    ConfirmDelete -->|確認| DeleteBook[🗑️ 刪除書籍]
    DeleteBook --> Home

    %% 搜尋與篩選
    Action -->|搜尋| Search[🔍 搜尋頁面]
    Search --> TypeKeyword[輸入關鍵字\n即時顯示結果]
    TypeKeyword --> Filter{加入篩選條件？}
    Filter -->|類別 / 評分 / 日期| FilterResult[📋 篩選後結果]
    Filter -->|不篩選| SearchResult[📋 搜尋結果]
    FilterResult --> ClickResult[點擊書籍]
    SearchResult --> ClickResult
    ClickResult --> Detail

    %% 統計儀表板
    Action -->|查看統計| Dashboard[📊 統計儀表板]
    Dashboard --> SwitchTime{切換時間範圍}
    SwitchTime -->|今年| YearStat[今年統計數據]
    SwitchTime -->|全部時間| AllStat[全部時間統計]

    %% 金句收藏
    Action -->|瀏覽金句| Quotes[💬 金句收藏庫]
    Quotes --> QuoteAction{金句操作}
    QuoteAction -->|隨機金句| RandomQuote[🎲 今日金句]
    QuoteAction -->|複製金句| CopyQuote[📋 複製成功提示]

    %% 標籤管理
    Action -->|管理標籤| Tags[🏷️ 標籤管理頁]
    Tags --> TagAction{標籤操作}
    TagAction -->|新增| AddTag[新增自訂標籤]
    TagAction -->|重新命名| RenameTag[修改標籤名稱]
    TagAction -->|刪除| ConfirmTagDelete{確認刪除？}
    ConfirmTagDelete -->|確認| DeleteTag[刪除標籤\n原書籍標籤清空]
    ConfirmTagDelete -->|取消| Tags

    %% 匯出
    Action -->|匯出資料| Export{選擇匯出格式}
    Export -->|CSV| DownloadCSV[⬇️ 下載 CSV 檔]
    Export -->|JSON| DownloadJSON[⬇️ 下載 JSON 檔]
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 新增書籍完整流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(books.py)
    participant Model as SQLAlchemy Model\n(book.py)
    participant DB as SQLite\n(database.db)

    User->>Browser: 點擊「新增筆記」
    Browser->>Flask: GET /books/create
    Flask-->>Browser: 回傳 create.html（空白表單）

    User->>Browser: 填寫表單並點擊「儲存」
    Browser->>Flask: POST /books/create（表單資料）

    Flask->>Flask: 驗證必填欄位
    alt 驗證失敗
        Flask-->>Browser: 回傳 create.html（含錯誤訊息）
        Browser-->>User: 顯示欄位錯誤提示
    else 驗證成功
        Flask->>Model: Book(**form_data)
        Model->>DB: INSERT INTO books (...)
        DB-->>Model: 新書籍 id = 42
        Model-->>Flask: book 物件
        Flask-->>Browser: 302 Redirect → GET /books/42
        Browser->>Flask: GET /books/42
        Flask->>Model: Book.query.get(42)
        Model->>DB: SELECT * FROM books WHERE id=42
        DB-->>Model: 書籍資料
        Model-->>Flask: book 物件
        Flask-->>Browser: 回傳 detail.html + Toast 通知
        Browser-->>User: 顯示詳細頁（新增成功）
    end
```

---

### 2.2 即時搜尋流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器\n(search.js)
    participant Flask as Flask Route\n(search.py)
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    User->>Browser: 輸入關鍵字（逐字觸發）
    Browser->>Browser: debounce 300ms

    Browser->>Flask: GET /search?q=關鍵字&category=科技
    Flask->>Model: Book.query.filter(\n  title.contains(q) OR\n  author.contains(q) OR\n  review.contains(q)\n)
    Model->>DB: SELECT ... WHERE ... LIKE '%q%'
    DB-->>Model: 符合的書籍列表
    Model-->>Flask: books 列表
    Flask-->>Browser: JSON 回應（書籍清單）
    Browser-->>User: 即時更新搜尋結果（關鍵字高亮）
```

---

### 2.3 刪除書籍流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(books.py)
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    User->>Browser: 點擊「刪除」按鈕
    Browser-->>User: 顯示確認對話框

    alt 使用者取消
        User->>Browser: 點擊「取消」
        Browser-->>User: 關閉對話框，留在詳細頁
    else 使用者確認
        User->>Browser: 點擊「確認刪除」
        Browser->>Flask: POST /books/42/delete
        Flask->>Model: Book.query.get(42).delete()
        Model->>DB: DELETE FROM books WHERE id=42\n（CASCADE 同步刪除 book_tags）
        DB-->>Model: 成功
        Model-->>Flask: 完成
        Flask-->>Browser: 302 Redirect → GET /books
        Browser-->>User: 跳回清單頁（書籍已移除）
    end
```

---

### 2.4 匯出資料流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(export.py)
    participant Model as SQLAlchemy Model
    participant DB as SQLite

    User->>Browser: 點擊「匯出 CSV」
    Browser->>Flask: GET /export/csv
    Flask->>Model: Book.query.all()
    Model->>DB: SELECT * FROM books
    DB-->>Model: 所有書籍資料
    Model-->>Flask: books 列表
    Flask->>Flask: 產生 CSV 內容\n檔名：reading_notes_20260425.csv
    Flask-->>Browser: 回應 Content-Disposition: attachment
    Browser-->>User: 自動下載 CSV 檔案
```

---

## 3. 功能清單對照表

| 功能 | 頁面說明 | URL 路徑 | HTTP 方法 |
|------|----------|----------|-----------|
| 首頁 / 書籍清單 | 以卡片顯示所有書籍，支援排序 | `/` 或 `/books` | `GET` |
| 新增書籍表單頁 | 顯示空白表單 | `/books/create` | `GET` |
| 新增書籍（送出） | 接收表單資料，寫入資料庫 | `/books/create` | `POST` |
| 書籍詳細頁 | 顯示單筆完整書籍資料 | `/books/<id>` | `GET` |
| 編輯書籍表單頁 | 表單預填原始資料 | `/books/<id>/edit` | `GET` |
| 編輯書籍（送出） | 更新資料庫中的書籍資料 | `/books/<id>/edit` | `POST` |
| 刪除書籍 | 刪除書籍及其關聯標籤 | `/books/<id>/delete` | `POST` |
| 搜尋頁面 | 顯示搜尋與篩選介面 | `/search` | `GET` |
| 搜尋 API | 回傳符合條件的書籍（JSON） | `/search?q=&category=` | `GET` |
| 統計儀表板 | 顯示閱讀統計與圖表 | `/dashboard` | `GET` |
| 金句收藏庫 | 顯示所有金句卡片 | `/quotes` | `GET` |
| 隨機金句 API | 回傳一則隨機金句（JSON） | `/quotes/random` | `GET` |
| 標籤管理頁 | 列出所有標籤，可新增/刪除 | `/tags` | `GET` |
| 新增標籤 | 建立新標籤 | `/tags/create` | `POST` |
| 重新命名標籤 | 更新標籤名稱 | `/tags/<id>/edit` | `POST` |
| 刪除標籤 | 刪除標籤（書籍標籤欄清空） | `/tags/<id>/delete` | `POST` |
| 匯出 CSV | 下載所有書籍資料（CSV 格式） | `/export/csv` | `GET` |
| 匯出 JSON | 下載所有書籍資料（JSON 格式） | `/export/json` | `GET` |

---

*本文件為 v1.0 草稿，如有修改請更新版本號與日期。*
