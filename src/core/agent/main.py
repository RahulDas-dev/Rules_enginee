import logging
import re
from typing import Dict, List, Mapping, Optional, Tuple

from litellm import token_counter

from src.core.client import ClientFactory
from src.core.executator import Executator

from .base import BaseMember
from .schemas import TestResult

logger = logging.getLogger(__name__)


class Agent(BaseMember):
    _name: str
    _system_msg: str
    _examples: List[Dict[str, str]]
    _chat_history: List[Dict[str, str]]
    _llm_config: Optional[Dict]

    def __init__(
        self,
        system_message: str = "You are a helpful AI Assistant.",
        llm_config: Optional[Dict] = None,
        examples: Optional[List[Dict]] = None,
        enable_cache: bool = True,
        enable_logger: bool = True,
    ):
        self._system_msg = system_message
        self._examples = [] if examples is None else examples
        if len(self._examples) % 2 != 0:
            raise ValueError("Examples is always multiple of 2")
        self._chat_history = [
            {"role": "system", "content": self._system_msg},
            *self._examples,
        ]
        self._enable_cache = enable_cache
        self._enable_logger = enable_logger
        self._llm_config = llm_config.copy() if llm_config is not None else {}

        self._client = ClientFactory.build(
            self._llm_config,
            self._enable_cache,
            self._enable_logger,
        )
        self._data_sets = []

    @property
    def has_chat_history(self) -> bool:
        return len(self._chat_history) > len(self._examples) + 1

    @property
    def model_name(self) -> str:
        return self._llm_config.get("model", "gpt-3.5-turbo")

    def set_data(self, data_sets: list[Mapping]) -> None:
        self._data_sets = data_sets

    def _generate_reply(self) -> Optional[Dict[str, str]]:
        # messages_t = self._format_message(messages)
        # self._chat_history.append(messages_t)
        response = self._client.response(self._chat_history)
        if response is not None:
            self._chat_history.append({"role": "assistant", "content": response.get("content", "")})
        return response

    def _format_message(self, messages: Dict[str, str]) -> Dict[str, str]:
        return messages.copy()

    def resolve_task(self, task: str) -> Tuple[str, str, list]:
        message = {"role": "user", "content": task}
        messages_t = self._format_message(message)
        self._chat_history.append(messages_t)
        response, code_content, test_results = None, None, []
        while True:
            response = self._generate_reply()
            if response is None or response.get("content", None) is None:
                return None, None
            code_content = self._perse_response(response.get("content", ""))
            if code_content is None:
                continue
            test_results, error_msg = self._execute_code(code_content)
            if error_msg is None:
                break
        return response, code_content, test_results

    def _extract_result_from_chat(self) -> Optional[str]:
        return self._chat_history[-1].get("content", None)

    @property
    def chat_history(self) -> List[Dict[str, str]]:
        """Returns the Chat history"""
        return self._chat_history.copy()

    def reset_chat_history(self) -> None:
        self._chat_history = [
            {"role": "system", "content": self._system_msg},
            *self._examples.copy(),
        ]

    def _perse_response(self, response: str) -> Optional[str]:
        if response is None or response == "":
            return None
        try:
            pattern = r"<pyfunction>(.*?)</pyfunction>"
            matche = re.search(pattern, response, re.DOTALL)
            code_content = matche.group(1).strip() if matche is not None else None
        except Exception as err:
            logger.error(f"Error while parsing response {err}")
            message = f"Error while parsing response, Error - {err}"
            self._chat_history.append({"role": "user", "content": message})
        else:
            if code_content is None:
                self._chat_history.append(
                    {
                        "role": "user",
                        "content": "Response Shoule be valid Xml format. pyfunction Should contain code",
                    }
                )
        return code_content

    def _execute_code(self, code_content: str) -> Tuple[list[TestResult], Optional[str]]:
        if not self._data_sets:
            return [], None
        executor = Executator(code_content)
        test_results = []
        for item in self._data_sets:
            status, resason, error = executor.execute(item.get("data", {}))
            result = TestResult(
                data_id=item.get("id", None),
                status=status,
                resason=resason,
                error=error,
            )
            test_results.append(result)

        if all(result.error is None for result in test_results):
            return test_results, None
        errors = [result.error for result in test_results if result.error is not None]
        err_msg = "\n".join([f"{idx + 1}. {error}" for idx, error in enumerate(errors)])
        self._chat_history.append(
            {
                "role": "user",
                "content": f"Error While excutating function, Error are {err_msg} kindly fix the errors and try again",
            }
        )
        return test_results, err_msg

    def count_tokens(self) -> int:
        return token_counter(model=self._llm_config.get("model", "gpt-3.5-turbo"), messages=self._chat_history)
