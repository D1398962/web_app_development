from datetime import datetime, date
from flask import Blueprint, render_template, request, jsonify
from app.models.book import Book
from app.models.tag import Tag

search_bp = Blueprint("search", __name__, url_prefix="/search")


@search_bp.route("/", methods=["GET"])
def index():
    """搜尋頁面

    Query 參數：
        q (str): 關鍵字（選填，有值時顯示初始搜尋結果）
    """
    q = request.args.get("q", "").strip()
    tags = Tag.get_all()
    books = Book.search(keyword=q) if q else []
    return render_template("search/index.html", books=books, tags=tags, q=q)


@search_bp.route("/api", methods=["GET"])
def api():
    """即時搜尋 API（回傳 JSON）

    Query 參數：
        q            (str):   全文搜尋關鍵字
        category_ids (list):  標籤 id 清單（可多值）
        rating_min   (float): 最低評分，預設 1.0
        rating_max   (float): 最高評分，預設 5.0
        date_from    (str):   起始日期 YYYY-MM-DD（選填）
        date_to      (str):   結束日期 YYYY-MM-DD（選填）
        is_recommend (str):   'true' / 'false' / 'all'
    """
    q            = request.args.get("q", "").strip()
    category_ids = [int(i) for i in request.args.getlist("category_ids") if i.isdigit()]
    is_recommend_str = request.args.get("is_recommend", "all")

    try:
        rating_min = float(request.args.get("rating_min", 1.0))
        rating_max = float(request.args.get("rating_max", 5.0))
        if not (1.0 <= rating_min <= 5.0 and 1.0 <= rating_max <= 5.0):
            raise ValueError
    except ValueError:
        return jsonify({"error": "評分範圍不合法"}), 400

    date_from = date_to = None
    try:
        if request.args.get("date_from"):
            date_from = date.fromisoformat(request.args.get("date_from"))
        if request.args.get("date_to"):
            date_to = date.fromisoformat(request.args.get("date_to"))
    except ValueError:
        return jsonify({"error": "日期格式不正確"}), 400

    is_recommend = None
    if is_recommend_str == "true":
        is_recommend = True
    elif is_recommend_str == "false":
        is_recommend = False

    books = Book.search(
        keyword=q,
        category_ids=category_ids or None,
        rating_min=rating_min,
        rating_max=rating_max,
        date_from=date_from,
        date_to=date_to,
        is_recommend=is_recommend,
    )

    return jsonify({
        "q": q,
        "count": len(books),
        "books": [
            {
                "id":          b.id,
                "title":       b.title,
                "author":      b.author,
                "rating":      b.rating,
                "finished_at": str(b.finished_at),
                "tags":        [t.name for t in b.tags],
                "cover_url":   b.cover_url or "",
                "is_recommend": b.is_recommend,
            }
            for b in books
        ],
    })
