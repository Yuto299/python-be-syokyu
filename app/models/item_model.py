# 「DBのテーブル定義」
from typing import ClassVar

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, text

from app.database import Base


class ItemModel(Base):
    """アイテムモデル."""

    __tablename__ = "todo_items"
    __table_args__: ClassVar[dict[str]] = {
        "comment": "アイテムテーブル",
    }

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    todo_list_id = Column(
        "todo_list_id", Integer, ForeignKey("todo_lists.id"), nullable=False
    )
    title = Column("title", String(50), nullable=False)
    description = Column("description", String(200))
    status_code = Column("status_code", Integer)
    due_at = Column("due_at", DateTime)
    created_at = Column("created_at", DateTime, server_default=func.now())
    updated_at = Column(
        "updated_at",
        DateTime,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
