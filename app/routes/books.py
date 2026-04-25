from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app import db
from app.models.book import Book
from app.models.tag import Tag

books_bp = Blueprint("books", __name__, url_prefix="/books")


# ──────────────────────────────────────────────
# 工具函式
# ──────────────────────────────────────────────

def _parse_book_form(form):
    """從 request.form 解析書籍欄位，回傳 (data_dict, errors_dict)"""
    errors = {}

    title       = form.get("title", "").strip()
    author      = form.get("author", "").strip()
    finished_at = form.get("finished_at", "").strip()
    rating      = form.get("rating", "").strip()
    review      = form.get("review", "").strip()
    cover_url   = form.get("cover_url", "").strip() or None
    is_recommend = form.get("is_recommend") == "on"
    quote       = form.get("quote", "").strip() or None
    page_count  = form.get("page_count", "").strip() or None
    tag_ids     = [int(i) for i in form.getlist("tag_ids") if i.isdigit()]

    # 必填驗證
    if not title:
        errors["title"] = "書名為必填"
    if not author:
        errors["author"] = "作者為必填"
    if not finished_at:
        errors["finished_at"] = "閱讀完成日期為必填"
    else:
        try:
            finished_at = date.fromisoformat(finished_at)
        except ValueError:
            errors["finished_at"] = "日期格式不正確（YYYY-MM-DD）"
    if not rating:
        errors["rating"] = "評分為必填"
    else:
        try:
            rating = float(rating)
            if not (1.0 <= rating <= 5.0):
                errors["rating"] = "評分須介於 1 ~ 5 之間"
        except ValueError:
            errors["rating"] = "評分格式不正確"
    if not review:
        errors["review"] = "閱讀心得為必填"
    if page_count is not None:
        try:
            page_count = int(page_count)
        except ValueError:
            page_count = None

    data = {
        "title":        title,
        "author":       author,
        "finished_at":  finished_at,
        "rating":       rating,
        "review":       review,
        "cover_url":    cover_url,
        "is_recommend": is_recommend,
        "quote":        quote,
        "page_count":   page_count,
        "tag_ids":      tag_ids,
    }
    return data, errors


# ──────────────────────────────────────────────
# 路由
# ──────────────────────────────────────────────

@books_bp.route("/", methods=["GET"])
def index():
    """書籍清單頁

    Query 參數：
        sort_by (str): 排序欄位，預設 'created_at'
        order   (str): 排序方向 'asc' / 'desc'，預設 'desc'
    """
    allowed_sort = {"created_at", "finished_at", "rating", "title"}
    sort_by = request.args.get("sort_by", "created_at")
    order   = request.args.get("order", "desc")

    if sort_by not in allowed_sort:
        sort_by = "created_at"
    if order not in ("asc", "desc"):
        order = "desc"

    books = Book.get_all(sort_by=sort_by, order=order)
    return render_template("books/list.html", books=books, sort_by=sort_by, order=order)


@books_bp.route("/create", methods=["GET"])
def create_form():
    """顯示新增書籍表單頁"""
    tags = Tag.get_all()
    return render_template("books/create.html", tags=tags, errors={}, form={}, selected_tag_ids=set())


@books_bp.route("/create", methods=["POST"])
def create():
    """接收新增書籍表單並寫入資料庫"""
    data, errors = _parse_book_form(request.form)

    if errors:
        tags = Tag.get_all()
        selected_tag_ids = {int(i) for i in request.form.getlist("tag_ids") if i.isdigit()}
        return render_template(
            "books/create.html",
            tags=tags,
            errors=errors,
            form=request.form,
            selected_tag_ids=selected_tag_ids,
        ), 422

    book = Book.create(**data)
    flash("✅ 書籍筆記新增成功！", "success")
    return redirect(url_for("books.detail", book_id=book.id))


@books_bp.route("/<int:book_id>", methods=["GET"])
def detail(book_id):
    """書籍詳細頁"""
    book = Book.get_by_id(book_id)
    if book is None:
        abort(404)
    return render_template("books/detail.html", book=book)


@books_bp.route("/<int:book_id>/edit", methods=["GET"])
def edit_form(book_id):
    """顯示編輯書籍表單頁（預填原始資料）"""
    book = Book.get_by_id(book_id)
    if book is None:
        abort(404)
    tags = Tag.get_all()
    selected_tag_ids = {t.id for t in book.tags}
    return render_template(
        "books/edit.html",
        book=book,
        tags=tags,
        selected_tag_ids=selected_tag_ids,
        errors={},
    )


@books_bp.route("/<int:book_id>/edit", methods=["POST"])
def edit(book_id):
    """接收編輯書籍表單並更新資料庫"""
    book = Book.get_by_id(book_id)
    if book is None:
        abort(404)

    data, errors = _parse_book_form(request.form)

    if errors:
        tags = Tag.get_all()
        selected_tag_ids = {t.id for t in book.tags}
        return render_template(
            "books/edit.html",
            book=book,
            tags=tags,
            selected_tag_ids=selected_tag_ids,
            errors=errors,
        ), 422

    book.update(**data)
    flash("✅ 書籍筆記已更新！", "success")
    return redirect(url_for("books.detail", book_id=book.id))


@books_bp.route("/<int:book_id>/delete", methods=["POST"])
def delete(book_id):
    """刪除書籍"""
    book = Book.get_by_id(book_id)
    if book is None:
        abort(404)
    book.delete()
    flash("🗑️ 書籍筆記已刪除。", "info")
    return redirect(url_for("books.index"))
