import csv
import json
import io
from datetime import date
from flask import Blueprint, make_response
from app.models.book import Book

export_bp = Blueprint("export", __name__, url_prefix="/export")


def _filename(ext):
    """產生帶今日日期的檔名"""
    today = date.today().strftime("%Y%m%d")
    return f"reading_notes_{today}.{ext}"


@export_bp.route("/csv", methods=["GET"])
def export_csv():
    """匯出所有書籍資料為 CSV 檔案"""
    books = Book.export_all()

    output = io.StringIO()
    fieldnames = [
        "id", "title", "author", "finished_at", "rating",
        "review", "cover_url", "is_recommend", "quote",
        "page_count", "tags", "created_at", "updated_at",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(books)

    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8-sig"
    response.headers["Content-Disposition"] = (
        f'attachment; filename="{_filename("csv")}"'
    )
    return response


@export_bp.route("/json", methods=["GET"])
def export_json():
    """匯出所有書籍資料為 JSON 檔案"""
    books = Book.export_all()

    response = make_response(
        json.dumps(books, ensure_ascii=False, indent=2)
    )
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.headers["Content-Disposition"] = (
        f'attachment; filename="{_filename("json")}"'
    )
    return response
