from app.routes.books import books_bp
from app.routes.search import search_bp
from app.routes.dashboard import dashboard_bp
from app.routes.quotes import quotes_bp
from app.routes.tags import tags_bp
from app.routes.export import export_bp

__all__ = [
    "books_bp",
    "search_bp",
    "dashboard_bp",
    "quotes_bp",
    "tags_bp",
    "export_bp",
]
