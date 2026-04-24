from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

tags_bp = Blueprint("tags", __name__, url_prefix="/tags")


@tags_bp.route("/", methods=["GET"])
def index():
    """標籤管理頁面

    回傳：
        渲染 tags/index.html，傳入 tags 列表
        每個 tag 附帶 book_count（使用該標籤的書籍數量）
    """
    pass


@tags_bp.route("/create", methods=["POST"])
def create():
    """新增標籤

    表單欄位：
        name (str): 標籤名稱（必填，不可重複）

    回傳：
        成功 → redirect 到 GET /tags
        名稱重複 → flash 錯誤訊息，redirect 回 GET /tags
    """
    pass


@tags_bp.route("/<int:tag_id>/edit", methods=["POST"])
def edit(tag_id):
    """重新命名標籤

    Args:
        tag_id (int): 標籤 id

    表單欄位：
        name (str): 新標籤名稱（必填）

    回傳：
        成功 → redirect 到 GET /tags
        標籤不存在 → 404
        名稱重複 → flash 錯誤訊息，redirect 回 GET /tags
    """
    pass


@tags_bp.route("/<int:tag_id>/delete", methods=["POST"])
def delete(tag_id):
    """刪除標籤

    Args:
        tag_id (int): 標籤 id

    回傳：
        成功 → redirect 到 GET /tags（原本含此標籤的書籍標籤欄清空）
        標籤不存在 → 404
    """
    pass
