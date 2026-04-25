import os
import markupsafe
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# 載入 .env 環境變數
load_dotenv()

# 建立全域 SQLAlchemy 實例（在 create_app 之前宣告，供 models 引用）
db = SQLAlchemy()


def create_app():
    """Flask Application Factory — 建立並設定 Flask app"""
    app = Flask(__name__, instance_relative_config=True)

    # ── 設定 ──────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{os.path.join(app.instance_path, 'database.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── 確保 instance 資料夾存在 ──────────────────────────
    os.makedirs(app.instance_path, exist_ok=True)

    # ── 初始化擴充套件 ────────────────────────────────────
    db.init_app(app)

    # ── 匯入 Models（讓 SQLAlchemy 建表時找得到） ─────────
    from app.models.book import Book  # noqa: F401
    from app.models.tag import Tag    # noqa: F401

    # ── 建立資料表（首次啟動自動建表） ───────────────────
    with app.app_context():
        db.create_all()
        _seed_default_tags()

    # ── 註冊 Blueprints ───────────────────────────────────
    from app.routes.books import books_bp
    from app.routes.search import search_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.quotes import quotes_bp
    from app.routes.tags import tags_bp
    from app.routes.export import export_bp

    app.register_blueprint(books_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(export_bp)

    # 首頁重導向到書籍清單
    from flask import redirect, url_for

    @app.route("/")
    def index():
        return redirect(url_for("books.index"))

    # ── 自訂 Jinja2 過濾器 ───────────────────────────────
    @app.template_filter("nl2br")
    def nl2br_filter(value):
        """將換行符號轉換為 HTML <br> 標籤"""
        if not value:
            return ""
        escaped = markupsafe.escape(value)
        return markupsafe.Markup(str(escaped).replace("\n", "<br>\n"))

    return app


def _seed_default_tags():
    """初始化預設標籤（若尚未存在）"""
    from app.models.tag import Tag

    default_tags = ["科技", "文學", "心理學", "商業", "歷史", "其他"]
    for name in default_tags:
        if not Tag.query.filter_by(name=name).first():
            db.session.add(Tag(name=name))
    db.session.commit()
