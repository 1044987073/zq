"""SQLite incremental index cache (HANDOFF §7 Step 2)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


class ImageIndexRow(Base):
    __tablename__ = "image_index"

    id = Column(Integer, primary_key=True, autoincrement=True)
    abs_path = Column(String, unique=True, index=True, nullable=False)
    file_mtime = Column(Float, nullable=False)
    file_size = Column(Integer, nullable=False)
    cache_key = Column(String, index=True, nullable=False)
    md5 = Column(String, nullable=True)
    indexed_at = Column(DateTime, default=datetime.utcnow)

    exif_datetime = Column(String, nullable=True)
    exif_gps_lat = Column(Float, nullable=True)
    exif_gps_lon = Column(Float, nullable=True)
    phash = Column(String, nullable=True)

    gray_mean = Column(Float, nullable=True)
    highlight_ratio = Column(Float, nullable=True)
    shadow_ratio = Column(Float, nullable=True)
    laplacian_full = Column(Float, nullable=True)

    faces_json = Column(JSON, nullable=True)
    error = Column(String, nullable=True)


def make_cache_key(abs_path: str, mtime: float, size: int) -> str:
    return f"{abs_path}|{mtime}|{size}"


class IndexDatabase:
    def __init__(self, db_path: Path) -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{db_path}", future=True)
        Base.metadata.create_all(self.engine)
        self._Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    def get_cached(self, abs_path: str, mtime: float, size: int) -> Optional[ImageIndexRow]:
        key = make_cache_key(abs_path, mtime, size)
        with self._Session() as session:
            row = session.query(ImageIndexRow).filter_by(cache_key=key).one_or_none()
            if row:
                session.expunge(row)
            return row

    def upsert(self, row_data: Dict[str, Any]) -> None:
        with self._Session() as session:
            existing = session.query(ImageIndexRow).filter_by(abs_path=row_data["abs_path"]).one_or_none()
            if existing:
                for k, v in row_data.items():
                    setattr(existing, k, v)
            else:
                session.add(ImageIndexRow(**row_data))
            session.commit()

    def count(self) -> int:
        with self._Session() as session:
            return session.query(ImageIndexRow).count()
