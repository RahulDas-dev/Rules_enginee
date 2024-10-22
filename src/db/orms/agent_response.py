from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Integer, String

from src.core.agent.schemas import ChatHistory, TestResult
from src.db.pydantic_col_type import PydanticColumn

from .base import Base


class AgentResponse(Base):
    __tablename__ = "agent_response"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    version: Mapped[str] = mapped_column(String(), nullable=False)
    rules_input: Mapped[str] = mapped_column(String(), nullable=False)
    agent_reponse: Mapped[str] = mapped_column(String(), nullable=False)
    code_content: Mapped[str] = mapped_column(String(), nullable=False, default="")
    chat_history: Mapped[ChatHistory] = mapped_column(
        PydanticColumn(ChatHistory),
        nullable=False,
        default=ChatHistory(),
    )
    test_results: Mapped[TestResult] = mapped_column(type_=PydanticColumn(TestResult), default="{}", nullable=False)
    token_count: Mapped[int] = mapped_column(Integer(), default=0, nullable=False)
    llm: Mapped[str] = mapped_column(String(), nullable=False)
    retry_count: Mapped[int] = mapped_column(Integer(), default=0, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())
