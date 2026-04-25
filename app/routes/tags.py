from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.tag import Tag

tags_bp = Blueprint("tags", __name__, url_prefix="/tags")


@tags_bp.route("/", methods=["GET"])
def index():
    """標籤管理頁面"""
    tags = Tag.get_all()
    # 附帶每個標籤的書籍數量
    tags_with_count = [{"tag": t, "book_count": len(t.books)} for t in tags]
    return render_template("tags/index.html", tags_with_count=tags_with_count)


@tags_bp.route("/create", methods=["POST"])
def create():
    """新增標籤"""
    name = request.form.get("name", "").strip()
    if not name:
        flash("⚠️ 標籤名稱不可為空。", "warning")
        return redirect(url_for("tags.index"))
    try:
        Tag.create(name)
        flash(f"✅ 標籤「{name}」新增成功！", "success")
    except ValueError as e:
        flash(str(e), "warning")
    return redirect(url_for("tags.index"))


@tags_bp.route("/<int:tag_id>/edit", methods=["POST"])
def edit(tag_id):
    """重新命名標籤"""
    tag = Tag.get_by_id(tag_id)
    if tag is None:
        abort(404)
    name = request.form.get("name", "").strip()
    if not name:
        flash("⚠️ 標籤名稱不可為空。", "warning")
        return redirect(url_for("tags.index"))
    try:
        tag.update(name)
        flash(f"✅ 標籤已更名為「{name}」。", "success")
    except ValueError as e:
        flash(str(e), "warning")
    return redirect(url_for("tags.index"))


@tags_bp.route("/<int:tag_id>/delete", methods=["POST"])
def delete(tag_id):
    """刪除標籤"""
    tag = Tag.get_by_id(tag_id)
    if tag is None:
        abort(404)
    name = tag.name
    tag.delete()
    flash(f"🗑️ 標籤「{name}」已刪除。", "info")
    return redirect(url_for("tags.index"))
