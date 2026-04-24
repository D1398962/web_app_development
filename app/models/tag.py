from app import db
from datetime import datetime


class Tag(db.Model):
    """標籤 Model — 對應 tags 資料表"""

    __tablename__ = "tags"

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.Text, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # 反向關聯（透過 book_tags）
    books = db.relationship("Book", secondary="book_tags", back_populates="tags")

    def __repr__(self):
        return f"<Tag id={self.id} name={self.name!r}>"

    # ----------------------------------------------------------
    # CRUD 方法
    # ----------------------------------------------------------

    @classmethod
    def get_all(cls):
        """取得所有標籤，依名稱排序"""
        return cls.query.order_by(cls.name).all()

    @classmethod
    def get_by_id(cls, tag_id):
        """依 id 取得單筆標籤，不存在則回傳 None"""
        return cls.query.get(tag_id)

    @classmethod
    def get_by_name(cls, name):
        """依名稱取得標籤，不存在則回傳 None"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def create(cls, name):
        """建立新標籤，若名稱重複則拋出 ValueError"""
        if cls.get_by_name(name):
            raise ValueError(f"標籤「{name}」已存在")
        tag = cls(name=name)
        db.session.add(tag)
        db.session.commit()
        return tag

    def update(self, name):
        """更新標籤名稱"""
        if Tag.get_by_name(name) and Tag.get_by_name(name).id != self.id:
            raise ValueError(f"標籤「{name}」已存在")
        self.name = name
        db.session.commit()
        return self

    def delete(self):
        """刪除標籤（book_tags 關聯列同步刪除，書籍本身不受影響）"""
        db.session.delete(self)
        db.session.commit()
