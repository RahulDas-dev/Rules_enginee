import logging
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class Executator:
    def __init__(self, code_content: str):
        self._code = code_content
        self.namespace = {}
        exec(self._code, self.namespace)  # noqa: S102
        function = self.namespace.get("evaluate_credit_score", None)
        if callable(function):
            self.function = function
            logger.info("Function Loaded Successfully")
        else:
            self.function = None
            logger.info("Function not Loaded Successfully")

    def execute(self, data: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        status, reason, error = None, None, None
        if self.function is None:
            logger.info("Function not Loaded Successfully")
            return None
        try:
            status = self.function(data)
        except KeyError as e:
            logger.error(f"KeyError while evaluating rule: {e}")
            error = f"KeyError: {e} "
            status, reason = None, None
        except Exception as e:
            logger.error(f"Error details: {e}")
            error = f"Error: {e}"
            status, reason = None, None
        return status, reason, error
