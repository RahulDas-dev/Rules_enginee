from src.core.agent import SYSTEM_MESSAGE, TASK, Agent
from src.core.agent.schemas import AgentResponse, ChatHistory
from src.db.orms import DataSets


class RulesBuilder:
    def __init__(self, version: str, rules_str: str, json_schema: str):
        self.version = version
        self.rules_str = rules_str
        self.agent = Agent(
            system_message=SYSTEM_MESSAGE.format(RULES=rules_str, JSON_SCHEMA=json_schema),
            llm_config={"model": "gpt-4o"},
            examples=None,
            enable_cache=False,
            enable_logger=True,
        )

    def build(self, dataset: DataSets) -> AgentResponse:
        self.agent.set_data(dataset)
        response, code_content, test_results = self.agent.resolve_task(TASK)
        return AgentResponse(
            version=self.version,
            agent_reponse=response.get("content", ""),
            code_content=code_content,
            token_count=self.agent.count_tokens(),
            chat_history=ChatHistory(chat_history=self.agent.chat_history),
            llm=self.agent.model_name,
            test_results=test_results,
        )
