"""
讀書筆記本系統 — 應用程式入口

執行方式：
    python app.py
    或
    flask run
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
