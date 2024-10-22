from typing import Any, Dict, Literal

from .llmclient import LlmClient

ClientType = Literal["Gemeni", "claude-3-opus", "codechat-bison", "Gemini"]


DEFAULT_CONFIG = {
    "temperature": 0.1,
    "timeout": 600,
    "num_retries": 3,
}

GPT4O_DEFAULT_CONFIG = {**DEFAULT_CONFIG, "max_tokens": 4096}

ANTHROPIC_DEFAULT_CONFIG = {**DEFAULT_CONFIG, "max_tokens": 4096}

GEMINI_DEFAULT_CONFIG = {**DEFAULT_CONFIG, "max_tokens": 4096}


class ClientFactory:
    @staticmethod
    def build(config: Dict[str, Any], enenable_cache: bool = False, enable_logger: bool = True) -> LlmClient:
        config_ = config.copy()
        # client_type: ClientType = config_.get("model", None)
        config_ = {**DEFAULT_CONFIG, **config}
        return LlmClient(config_, enenable_cache, enable_logger)
