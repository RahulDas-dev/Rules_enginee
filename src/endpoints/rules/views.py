import logging
from typing import Mapping

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import UJSONResponse
from sqlalchemy.orm import Session

from src.core.agent.schemas import Version
from src.db.curd.data_model import get_data_model_by_version
from src.db.curd.dataset import get_latest_datasets
from src.db.curd.rules_info import get_latest_rules_info, insert_rules_info
from src.db.provider import get_db_session
from src.endpoints.rules.builder import RulesBuilder
from src.endpoints.rules.schemas import RequestBody, ResponseBody

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/latest_vesion", response_model=ResponseBody)
def latest_vesion(session: Session = Depends(get_db_session)) -> Mapping[str, str]:
    latest_rules = get_latest_rules_info(session)
    curent_version = "1.0" if latest_rules is None else latest_rules.version
    rules_str = "" if latest_rules is None else latest_rules.rules_str
    next_version = [
        Version.from_str(curent_version).upadate_version().to_str(),
        Version.from_str(curent_version).update_major_version().to_str(),
    ]
    content_ = {
        "version": curent_version,
        "next_versions": next_version,
        "rules_str": rules_str,
    }
    return UJSONResponse(status_code=status.HTTP_200_OK, content=content_)


@router.post("/new/", status_code=status.HTTP_201_CREATED)
def new(reqwstbdy: RequestBody = Body(), session: Session = Depends(get_db_session)) -> Mapping[str, str]:
    logger.info(f"Session id: {id(session)} | Request body: {reqwstbdy.version} ")
    dataset = get_latest_datasets(session)
    if len(dataset) == 0:
        logger.error(f"Session id: {id(session)} | No datasets Found")
        return UJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=[{"query": "None", "error": "No datasets Found"}],
        )
    logger.info(f"Session id: {id(session)} | Dataset count: {len(dataset)}")
    datamodel = get_data_model_by_version(session, "1.0")
    if datamodel is None:
        logger.error(f"Session id: {id(session)} | No datasets Found")
        return UJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=[{"query": "None", "error": "No DataModel Found"}],
        )
    # logger.info(f"Session id: {id(session)} | schema {datamodel.schema}")
    try:
        rules_builder = RulesBuilder(
            version=reqwstbdy.version, rules_str=reqwstbdy.rules_str, json_schema=datamodel.get_schema()
        )
        logger.info(f"Session id: {id(session)} | rules_builder initiated")
        datsets = [item.as_dict() for item in dataset]
        response = rules_builder.build(datsets)
        logger.info(f"Session id: {id(session)} | rules Created")
    except Exception as e:
        logger.error(f"Session id: {id(session)} | Error while creating rules, Error - {e}")
    else:
        if response is None or response.code_content is None:
            return UJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.code_content)
        session.commit()
        insert_dict = {
            "version": response.version,
            "rules_input": reqwstbdy.rules_str,
            "agent_reponse": response.agent_reponse,
            "code_content": response.code_content,
            "chat_history": response.chat_history,
            "test_results": response.test_results,
            "token_count": response.token_count,
            "llm": response.llm,
            "retry_count": 0,
        }
        action_info = insert_rules_info(session, insert_dict=insert_dict)
        if action_info is None:
            logger.error(f"Session id: {id(session)} | rules Creation Failed")
    return UJSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="Rules Created Successfully",
    )
