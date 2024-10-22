import copy
from datetime import datetime
from typing import Any, Dict, Optional

import ujson
from sqlalchemy import JSON, Index, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from .base import Base


class DataModel(Base):
    __tablename__ = "data_model"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    version: Mapped[str] = mapped_column(String(), nullable=False)
    schema: Mapped[Dict[str, Any]] = mapped_column(type_=JSON, default="{}", nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())

    __table_args__ = (Index("data_model_vesrion_index", version),)

    def get_data_json_str(self) -> str:
        return ujson.dumps(self.data)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "schema": self.schema,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def get_schema(self) -> Dict[str, Any]:
        return copy.deepcopy(self.schema)
