import random
from flask import Blueprint, render_template, jsonify
from app.models.book import Book

quotes_bp = Blueprint("quotes", __name__, url_prefix="/quotes")


@quotes_bp.route("/", methods=["GET"])
def index():
    """金句收藏庫頁面"""
    books = Book.get_with_quotes()
    return render_template("quotes/index.html", books=books)


@quotes_bp.route("/random", methods=["GET"])
def random_quote():
    """隨機金句 API（回傳 JSON）"""
    books = Book.get_with_quotes()
    if not books:
        return jsonify({"error": "尚無任何金句"}), 404
    book = random.choice(books)
    return jsonify({
        "quote":  book.quote,
        "title":  book.title,
        "author": book.author,
    })
