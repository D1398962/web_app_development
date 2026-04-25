from datetime import datetime
from flask import Blueprint, render_template, request
from app.models.book import Book
from app.models.tag import Tag
from app import db

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/", methods=["GET"])
def index():
    """統計儀表板

    Query 參數：
        period (str): 時間範圍 'year'（今年，預設）/ 'all'（全部時間）
    """
    period = request.args.get("period", "year")
    if period not in ("year", "all"):
        period = "year"

    now = datetime.now()
    year, month = now.year, now.month

    # ── 基本統計 ──────────────────────────────────────────
    total_books = Book.count_all()
    month_books = Book.count_by_month(year, month)
    year_books  = Book.count_by_year(year)
    avg_rating  = Book.average_rating()
    top_books   = Book.top_rated(limit=3)

    # ── 類別分佈（圓餅圖） ────────────────────────────────
    tags = Tag.get_all()
    category_data = {
        "labels": [],
        "values": [],
    }
    for tag in tags:
        count = len(tag.books)
        if count > 0:
            category_data["labels"].append(tag.name)
            category_data["values"].append(count)

    # ── 每月閱讀趨勢（過去 12 個月，折線圖） ─────────────
    monthly_trend = []
    for i in range(11, -1, -1):
        m = month - i
        y = year
        while m <= 0:
            m += 12
            y -= 1
        cnt = Book.count_by_month(y, m)
        monthly_trend.append({
            "label": f"{y}/{m:02d}",
            "count": cnt,
        })

    return render_template(
        "dashboard/index.html",
        total_books=total_books,
        month_books=month_books,
        year_books=year_books,
        avg_rating=avg_rating,
        top_books=top_books,
        category_data=category_data,
        monthly_trend=monthly_trend,
        period=period,
        current_year=year,
    )
