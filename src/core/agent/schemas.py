from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    role: Literal["assistant", "user", "system"]
    content: Optional[str]


class ChatHistory(BaseModel):
    chat_history: list[ChatMessage] = Field(default_factory=list)


class TestResult(BaseModel):
    data_id: int
    status: Optional[str]
    resason: Optional[str]
    error: Optional[str]

    @classmethod
    def is_status_valid(cls, status: str) -> bool:
        return status.lower() in ["rejected", "not rejected", "notrejected", "not-rejected"]


class AgentResponse(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    version: str = Field(description="The version of the model used to generate the response.")
    agent_reponse: str = Field(description="The response string to return to the user.")
    code_content: str = Field(description="The python code extracted from the response.")
    token_count: int = Field(
        description="The number of tokens used to generate the response.",
        default=0,
    )
    chat_history: ChatHistory = Field(
        description="The chat history used to generate the response.",
        default_factory=lambda: ChatHistory(chat_history=[]),
    )
    llm: str = Field(description="The language model used to generate the response.", default="gpt-3.5-turbo")
    test_results: list[TestResult] = Field(default_factory=list)


class Version(BaseModel):
    major: int = Field(default=0)
    minor: int = Field(default=0)

    @classmethod
    def from_str(cls, version: str) -> "Version":
        major, minor = version.split(".")
        return cls(major=int(major), minor=int(minor))

    def to_str(self) -> str:
        return f"{self.major}.{self.minor}"

    def upadate_version(self) -> "Version":
        return Version(major=self.major, minor=self.minor + 1)

    def update_major_version(self) -> "Version":
        return Version(major=self.major + 1, minor=0)
