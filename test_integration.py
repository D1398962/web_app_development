import json
from app import create_app, db
from app.models.book import Book
from app.models.tag import Tag

app = create_app()

print('=' * 50)
print('Step 5: Integration Tests')
print('=' * 50)

with app.test_client() as client:

    # ── 1. 主要頁面 ──────────────────────────────────────
    print('\n[1] 主要頁面載入')
    pages = [
        ('/',           302, '首頁重導向'),
        ('/books/',     200, '書籍清單'),
        ('/search/',    200, '搜尋頁'),
        ('/dashboard/', 200, '統計儀表板'),
        ('/quotes/',    200, '金句收藏'),
        ('/tags/',      200, '標籤管理'),
    ]
    for path, expected, name in pages:
        res = client.get(path)
        ok = res.status_code == expected
        print(f"  {'OK' if ok else 'FAIL'} {name} -> {res.status_code}")

    # ── 2. 新增書籍 ───────────────────────────────────────
    print('\n[2] 新增書籍')
    res = client.post('/books/create', data={})
    print(f"  {'OK' if res.status_code == 422 else 'FAIL'} 空表單驗證拒絕 -> {res.status_code}")

    res = client.post('/books/create', data={
        'title':       'Test Book: Atomic Habits',
        'author':      'James Clear',
        'finished_at': '2026-04-01',
        'rating':      '4.5',
        'review':      'Small habits, big results.',
        'quote':       'You do not rise to the level of your goals.',
    }, follow_redirects=False)
    print(f"  {'OK' if res.status_code == 302 else 'FAIL'} 新增成功並重導向 -> {res.status_code}")

    res = client.get('/books/')
    has_book = b'Atomic Habits' in res.data
    print(f"  {'OK' if has_book else 'FAIL'} 清單顯示新書籍")

    # ── 3. 取得 book_id ───────────────────────────────────
    with app.app_context():
        book = Book.query.filter_by(title='Test Book: Atomic Habits').first()
        book_id = book.id

    # ── 4. 詳細頁 ─────────────────────────────────────────
    print('\n[3] 詳細頁')
    res = client.get(f'/books/{book_id}')
    print(f"  {'OK' if res.status_code == 200 else 'FAIL'} 詳細頁正常顯示 -> {res.status_code}")
    print(f"  {'OK' if b'James Clear' in res.data else 'FAIL'} 作者正確顯示")
    res = client.get('/books/99999')
    print(f"  {'OK' if res.status_code == 404 else 'FAIL'} 不存在書籍回傳 404")

    # ── 5. 編輯書籍 ───────────────────────────────────────
    print('\n[4] 編輯書籍')
    res = client.get(f'/books/{book_id}/edit')
    print(f"  {'OK' if res.status_code == 200 else 'FAIL'} 編輯表單頁正常")

    res = client.post(f'/books/{book_id}/edit', data={
        'title':       'Test Book: Atomic Habits (Updated)',
        'author':      'James Clear',
        'finished_at': '2026-04-10',
        'rating':      '5.0',
        'review':      'Updated review content.',
    }, follow_redirects=False)
    print(f"  {'OK' if res.status_code == 302 else 'FAIL'} 編輯成功並重導向")

    res = client.get(f'/books/{book_id}')
    print(f"  {'OK' if b'Updated' in res.data else 'FAIL'} 詳細頁反映更新內容")

    # ── 6. 搜尋 API ───────────────────────────────────────
    print('\n[5] 搜尋功能')
    res = client.get('/search/api?q=Atomic')
    data = json.loads(res.data)
    print(f"  {'OK' if res.status_code == 200 else 'FAIL'} 搜尋 API 回應 200")
    print(f"  {'OK' if data['count'] >= 1 else 'FAIL'} 搜尋找到結果 (count={data['count']})")

    res = client.get('/search/api?q=XXXXXXNOTEXIST')
    data = json.loads(res.data)
    print(f"  {'OK' if data['count'] == 0 else 'FAIL'} 無結果正確回傳空列表")

    # ── 7. 統計儀表板 ─────────────────────────────────────
    print('\n[6] 統計儀表板')
    res = client.get('/dashboard/')
    print(f"  {'OK' if res.status_code == 200 else 'FAIL'} 儀表板頁面正常")
    print(f"  {'OK' if b'CHART_DATA' in res.data else 'FAIL'} 圖表資料嵌入頁面")

    # ── 8. 金句 API ───────────────────────────────────────
    print('\n[7] 金句功能')
    res = client.get('/quotes/')
    print(f"  {'OK' if res.status_code == 200 else 'FAIL'} 金句頁面正常")
    res = client.get('/quotes/random')
    data = json.loads(res.data)
    print(f"  {'OK' if res.status_code == 200 and 'quote' in data else 'FAIL'} 隨機金句 API 正常")

    # ── 9. 標籤管理 ───────────────────────────────────────
    print('\n[8] 標籤管理')
    res = client.post('/tags/create', data={'name': 'TestTag'}, follow_redirects=False)
    print(f"  {'OK' if res.status_code == 302 else 'FAIL'} 新增標籤成功")
    res = client.post('/tags/create', data={'name': 'TestTag'}, follow_redirects=False)
    print(f"  {'OK' if res.status_code == 302 else 'FAIL'} 重複標籤不拋出 500（有防護）")

    # ── 10. 匯出 ──────────────────────────────────────────
    print('\n[9] 資料匯出')
    res = client.get('/export/csv')
    print(f"  {'OK' if res.status_code == 200 else 'FAIL'} CSV 匯出成功")
    print(f"  {'OK' if b'title' in res.data else 'FAIL'} CSV 含標題列")
    cd = res.headers.get('Content-Disposition', '')
    print(f"  {'OK' if 'reading_notes' in cd else 'FAIL'} CSV 檔名格式正確")
    res = client.get('/export/json')
    print(f"  {'OK' if res.status_code == 200 else 'FAIL'} JSON 匯出成功")

    # ── 11. 刪除書籍 ──────────────────────────────────────
    print('\n[10] 刪除書籍')
    res = client.post(f'/books/{book_id}/delete', follow_redirects=False)
    print(f"  {'OK' if res.status_code == 302 else 'FAIL'} 刪除成功並重導向")

    res = client.get('/books/')
    print(f"  {'OK' if b'Atomic Habits' not in res.data else 'FAIL'} 清單已移除刪除的書籍")

    res = client.get(f'/books/{book_id}')
    print(f"  {'OK' if res.status_code == 404 else 'FAIL'} 已刪除書籍回傳 404")

print('\n' + '=' * 50)
print('All integration tests done.')
print('=' * 50)
