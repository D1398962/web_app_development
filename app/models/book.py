from app import db
from datetime import datetime


# 多對多關聯表（中間表）
book_tags = db.Table(
    "book_tags",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id",  ondelete="CASCADE"), primary_key=True),
    db.Column("tag_id",  db.Integer, db.ForeignKey("tags.id",   ondelete="CASCADE"), primary_key=True),
)


class Book(db.Model):
    """書籍筆記 Model — 對應 books 資料表"""

    __tablename__ = "books"

    id           = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    title        = db.Column(db.Text,     nullable=False)
    author       = db.Column(db.Text,     nullable=False)
    finished_at  = db.Column(db.Date,     nullable=False)
    rating       = db.Column(db.Float,    nullable=False)
    review       = db.Column(db.Text,     nullable=False)
    cover_url    = db.Column(db.Text,     nullable=True)
    is_recommend = db.Column(db.Boolean,  nullable=False, default=False)
    quote        = db.Column(db.Text,     nullable=True)
    page_count   = db.Column(db.Integer,  nullable=True)
    created_at   = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at   = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 多對多關聯
    tags = db.relationship("Tag", secondary="book_tags", back_populates="books")

    def __repr__(self):
        return f"<Book id={self.id} title={self.title!r}>"

    # ----------------------------------------------------------
    # CRUD 方法
    # ----------------------------------------------------------

    @classmethod
    def create(cls, title, author, finished_at, rating, review,
               cover_url=None, is_recommend=False, quote=None,
               page_count=None, tag_ids=None):
        """建立新書籍筆記"""
        book = cls(
            title=title,
            author=author,
            finished_at=finished_at,
            rating=rating,
            review=review,
            cover_url=cover_url,
            is_recommend=is_recommend,
            quote=quote,
            page_count=page_count,
        )
        if tag_ids:
            from app.models.tag import Tag
            book.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        db.session.add(book)
        db.session.commit()
        return book

    @classmethod
    def get_all(cls, sort_by="created_at", order="desc"):
        """取得所有書籍，支援排序

        sort_by 可為：'created_at'（預設）、'finished_at'、'rating'、'title'
        order   可為：'asc' 或 'desc'
        """
        column = getattr(cls, sort_by, cls.created_at)
        if order == "desc":
            column = column.desc()
        return cls.query.order_by(column).all()

    @classmethod
    def get_by_id(cls, book_id):
        """依 id 取得單筆書籍，不存在則回傳 None"""
        return cls.query.get(book_id)

    @classmethod
    def search(cls, keyword="", category_ids=None,
               rating_min=1.0, rating_max=5.0,
               date_from=None, date_to=None, is_recommend=None):
        """多條件搜尋書籍

        keyword      — 全文搜尋書名、作者、心得
        category_ids — 標籤 id 清單（多選）
        rating_min/max — 評分範圍
        date_from/to   — 閱讀日期區間
        is_recommend   — True/False/None（全部）
        """
        query = cls.query

        if keyword:
            like = f"%{keyword}%"
            query = query.filter(
                db.or_(
                    cls.title.ilike(like),
                    cls.author.ilike(like),
                    cls.review.ilike(like),
                )
            )

        if category_ids:
            from app.models.tag import Tag
            query = query.filter(cls.tags.any(Tag.id.in_(category_ids)))

        query = query.filter(cls.rating >= rating_min, cls.rating <= rating_max)

        if date_from:
            query = query.filter(cls.finished_at >= date_from)
        if date_to:
            query = query.filter(cls.finished_at <= date_to)
        if is_recommend is not None:
            query = query.filter(cls.is_recommend == is_recommend)

        return query.order_by(cls.finished_at.desc()).all()

    def update(self, **kwargs):
        """更新書籍欄位，tag_ids 用來更新多對多標籤"""
        tag_ids = kwargs.pop("tag_ids", None)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        if tag_ids is not None:
            from app.models.tag import Tag
            self.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        self.updated_at = datetime.now()
        db.session.commit()
        return self

    def delete(self):
        """刪除書籍（book_tags 關聯列同步刪除）"""
        db.session.delete(self)
        db.session.commit()

    # ----------------------------------------------------------
    # 統計用查詢
    # ----------------------------------------------------------

    @classmethod
    def count_all(cls):
        """總書籍數"""
        return cls.query.count()

    @classmethod
    def count_by_month(cls, year, month):
        """指定年月的閱讀數"""
        return cls.query.filter(
            db.extract("year",  cls.finished_at) == year,
            db.extract("month", cls.finished_at) == month,
        ).count()

    @classmethod
    def count_by_year(cls, year):
        """指定年份的閱讀數"""
        return cls.query.filter(
            db.extract("year", cls.finished_at) == year
        ).count()

    @classmethod
    def average_rating(cls):
        """所有書籍的平均評分"""
        result = db.session.query(db.func.avg(cls.rating)).scalar()
        return round(result, 2) if result else 0.0

    @classmethod
    def top_rated(cls, limit=3):
        """評分最高的前 N 本書"""
        return cls.query.order_by(cls.rating.desc()).limit(limit).all()

    @classmethod
    def get_with_quotes(cls):
        """取得所有有填寫金句的書籍"""
        return cls.query.filter(cls.quote.isnot(None), cls.quote != "").all()

    @classmethod
    def export_all(cls):
        """匯出所有書籍資料（dict 格式，用於 CSV/JSON 匯出）"""
        books = cls.query.order_by(cls.finished_at.desc()).all()
        return [
            {
                "id":           b.id,
                "title":        b.title,
                "author":       b.author,
                "finished_at":  str(b.finished_at),
                "rating":       b.rating,
                "review":       b.review,
                "cover_url":    b.cover_url or "",
                "is_recommend": b.is_recommend,
                "quote":        b.quote or "",
                "page_count":   b.page_count or "",
                "tags":         ", ".join(t.name for t in b.tags),
                "created_at":   str(b.created_at),
                "updated_at":   str(b.updated_at),
            }
            for b in books
        ]
