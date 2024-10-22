import json
import logging
from pathlib import Path

from dotenv import load_dotenv

from src.core.agent.main import Agent
from src.core.agent.template import SYSTEM_MESSAGE, TASK
from src.core.dataloader import XmlLoader
from src.core.transformer import RemovePrefix

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s",
    # format="%(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

loading_status = load_dotenv(verbose=True)

logger = logging.getLogger(__name__)

logger.info(f"loading_status {loading_status}")

# data_path = "./data/sample/1af3f6c9-9010-4aa2-9488-7f54165f2dee.html"
# loder = XmlLoader.from_path(data_path)
# documents = RemovePrefix().transform(loder.document)
# JSON_DATA = json.dumps(documents, indent=4)
# print(JSON_DATA)
# sys_msg = SYSTEM_MESSAGE.format(RULES=RULES)

# sys_msg = "You Are Helpfull AI Assistant"

# task = f"Here is the one example Json data Kindly think step by step and Generate JSON Query for Data Transformation and Rule Evalutaions, \n {JSON_DATA}"  # noqa: E501
# task = "What is the JSON Query Language ?"

# os.environ["LITELLM_LOG"] = "DEBUG"

SCHEMA_PATH = Path() / "data" / "data_schema.json"
DATA_DIR = Path() / "data" / "sample"

config3 = {"model": "gpt-3.5-turbo", "timeout": 12000}
config2 = {"model": "gpt-4o"}
config1 = {"model": "claude-3-opus@20240229"}

rules_str = """
1. Score < 650 THEN Reject
    Rule: If the credit score is less than 650, the applicant is rejected.
2. More than 2 PAN IDs THEN Reject
    Rule: If there are more than two PAN IDs, the applicant is rejected.
3. TotalInquiries > 3 THEN Reject
    Rule: If the number of total inquiries exceeds 3, the applicant is rejected.
4. if any Account of AccountType Excluding Credit Cards
    a. SuitFiledStatus = Yes THEN Reject
    Rule: If any Account has a 'Suit Filed' status as 'Yes', the applicant is rejected.
    b. WriteOffAmount > 0 THEN Reject
    Rule: If any Account has a WriteOffAmount greater than 0, the applicant is rejected.
    c. PastDueAmount > 1,500 and DateReported < 12 months THEN Reject
    Rule: If any Account has a PastDueAmount greater than 1,500, and DateReported is within the last 12 months and the
    PaymentStatus in any of the past 12 months is one of the listed delinquency statuses, the applicant is rejected.
    d. AccountStatus in {WDF, SUB, DBT, etc.} THEN Reject
    Rule: If any account has a status in the listed statuses, the applicant is rejected.
    e. PastDueAmount > 1,500 and DateReported > 12 months THEN Reject
    Rule: If any Account has a PastDueAmount greater than 1,500, DateReported is more than 12 months ago, and
    PaymentStatus in any of the past 6 months indicates delinquency, the applicant is rejected.
5. if any Account of AccountType = Credit Card  and PastDueAmount > 5,000 THEN Reject
    Rule: If any credit card account has a PastDueAmount greater than 5,000, the applicant is rejected.
"""


with open(SCHEMA_PATH, "r") as f:
    json_schema = json.load(f)

data = []
data_id = 1
for file_path in DATA_DIR.glob("*.html"):
    loder = XmlLoader.from_path(file_path)
    d = RemovePrefix().transform(loder.document)
    data.append({"id": data_id, "data": d})
    data_id += 1

# agent = ActorLLM(name="QueryBuilder", system_message=sys_msg, llm_config=config2)
agent = Agent(
    system_message=SYSTEM_MESSAGE.format(RULES=rules_str, JSON_SCHEMA=json_schema),
    llm_config={"model": "gpt-4o"},
    enable_cache=False,
    enable_logger=True,
)

agent.set_data(data)
resp = agent.resolve_task(TASK)

# system_message = SYSTEM_MESSAGE.format(RULES=rules_str, JSON_SCHEMA=json_schema)

logger.info(resp[1])
