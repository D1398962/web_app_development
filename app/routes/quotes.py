from flask import Blueprint, render_template, jsonify

quotes_bp = Blueprint("quotes", __name__, url_prefix="/quotes")


@quotes_bp.route("/", methods=["GET"])
def index():
    """金句收藏庫頁面

    回傳：
        渲染 quotes/index.html，傳入含有金句的 books 列表
        無金句時傳入空列表，模板顯示空狀態提示
    """
    pass


@quotes_bp.route("/random", methods=["GET"])
def random_quote():
    """隨機金句 API（回傳 JSON）

    回傳：
        application/json — { quote (str), title (str), author (str) }
        無任何金句 → 404
    """
    pass
