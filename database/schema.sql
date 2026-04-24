-- ============================================================
-- 讀書筆記本系統 — SQLite 建表語法
-- 版本：v1.0
-- 建立日期：2026-04-25
-- ============================================================

-- 啟用外鍵約束（SQLite 預設關閉）
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- 資料表 1：books（書籍筆記）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS books (
    id           INTEGER  PRIMARY KEY AUTOINCREMENT,
    title        TEXT     NOT NULL,
    author       TEXT     NOT NULL,
    finished_at  DATE     NOT NULL,
    rating       REAL     NOT NULL CHECK(rating >= 1.0 AND rating <= 5.0),
    review       TEXT     NOT NULL,
    cover_url    TEXT,
    is_recommend BOOLEAN  NOT NULL DEFAULT FALSE,
    quote        TEXT,
    page_count   INTEGER,
    created_at   DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at   DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ------------------------------------------------------------
-- 資料表 2：tags（標籤）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tags (
    id         INTEGER  PRIMARY KEY AUTOINCREMENT,
    name       TEXT     NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ------------------------------------------------------------
-- 資料表 3：book_tags（書籍標籤多對多關聯）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS book_tags (
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    tag_id  INTEGER NOT NULL REFERENCES tags(id)  ON DELETE CASCADE,
    PRIMARY KEY (book_id, tag_id)
);

-- ------------------------------------------------------------
-- 預設標籤資料（初始化）
-- ------------------------------------------------------------
INSERT OR IGNORE INTO tags (name) VALUES
    ('科技'),
    ('文學'),
    ('心理學'),
    ('商業'),
    ('歷史'),
    ('其他');
