from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("/", methods=["GET"])
def index():
    """書籍清單頁（首頁）

    Query 參數：
        sort_by (str): 排序欄位，預設 'created_at'
        order   (str): 排序方向 'asc' / 'desc'，預設 'desc'

    回傳：
        渲染 books/list.html，傳入 books 列表
    """
    pass


@books_bp.route("/create", methods=["GET"])
def create_form():
    """顯示新增書籍表單頁

    回傳：
        渲染 books/create.html，傳入 tags 列表（供多選標籤使用）
    """
    pass


@books_bp.route("/create", methods=["POST"])
def create():
    """接收新增書籍表單並寫入資料庫

    表單欄位：
        title, author, finished_at, rating, review,
        cover_url (選填), is_recommend (選填), quote (選填),
        page_count (選填), tag_ids[] (選填)

    回傳：
        成功 → redirect 到 GET /books/<new_id>
        失敗 → 重新渲染 books/create.html 並顯示錯誤
    """
    pass


@books_bp.route("/<int:book_id>", methods=["GET"])
def detail(book_id):
    """書籍詳細頁

    Args:
        book_id (int): 書籍 id

    回傳：
        渲染 books/detail.html，傳入 book 物件
        書籍不存在 → 404
    """
    pass


@books_bp.route("/<int:book_id>/edit", methods=["GET"])
def edit_form(book_id):
    """顯示編輯書籍表單頁（預填原始資料）

    Args:
        book_id (int): 書籍 id

    回傳：
        渲染 books/edit.html，傳入 book 物件與 tags 列表
        書籍不存在 → 404
    """
    pass


@books_bp.route("/<int:book_id>/edit", methods=["POST"])
def edit(book_id):
    """接收編輯書籍表單並更新資料庫

    Args:
        book_id (int): 書籍 id

    表單欄位：同新增書籍

    回傳：
        成功 → redirect 到 GET /books/<book_id>
        失敗 → 重新渲染 books/edit.html 並顯示錯誤
        書籍不存在 → 404
    """
    pass


@books_bp.route("/<int:book_id>/delete", methods=["POST"])
def delete(book_id):
    """刪除書籍

    Args:
        book_id (int): 書籍 id

    回傳：
        成功 → redirect 到 GET /books
        書籍不存在 → 404
    """
    pass
