from datetime import datetime
from typing import Any, Dict, Optional

import ujson
from sqlalchemy import JSON, Index, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from .base import Base


class DataSets(Base):
    __tablename__ = "data_sets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    version: Mapped[str] = mapped_column(String(), nullable=False)
    dformat: Mapped[str] = mapped_column(String(), nullable=False)
    data: Mapped[Dict[str, Any]] = mapped_column(type_=JSON, default="{}", nullable=False)
    dmetadata: Mapped[Dict[str, Any]] = mapped_column(type_=JSON, default="{}", nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())

    __table_args__ = (Index("data_sets_vesrion_index", version),)

    def get_data_json_str(self) -> str:
        return ujson.dumps(self.data)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "dformat": self.dformat,
            "data": self.data,
            "dmetadata": self.dmetadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
