from flask import Blueprint, render_template, request, jsonify

search_bp = Blueprint("search", __name__, url_prefix="/search")


@search_bp.route("/", methods=["GET"])
def index():
    """搜尋頁面

    Query 參數：
        q (str): 關鍵字（選填，有值時顯示初始搜尋結果）

    回傳：
        渲染 search/index.html，傳入 books（初始結果）、tags、q
    """
    pass


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

    回傳：
        application/json — 書籍列表 + 關鍵字（供前端高亮使用）
        參數不合法 → 400 Bad Request
    """
    pass
