import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from src.db.orms.agent_response import AgentResponse

logger = logging.getLogger(__name__)


def get_agent_response(db: Session, rules_id: int) -> Optional[AgentResponse]:
    query_stmt = select(AgentResponse).where(AgentResponse.id == rules_id)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching AgentResponse, for id: {rules_id}, Error - {e}",
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched AgentResponse details for id: {rules_id}",
        )
    return data


def get_latest_agent_response(db: Session) -> Optional[AgentResponse]:
    query_stmt = select(AgentResponse).order_by(AgentResponse.created_at.desc()).limit(1)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching AgentResponse, Error - {e}",
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched latest AgentResponse",
        )
    return data


def get_agent_response_by_version(db: Session, version: int) -> Optional[AgentResponse]:
    query_stmt = select(AgentResponse).where(AgentResponse.version == version)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching AgentResponse, for version: {version}, Error - {e}",
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched AgentResponse for version : {version}",
        )
    return data


def insert_actions_info(db: Session, insert_dict: dict) -> Optional[AgentResponse]:
    insert_dict_ = {
        **insert_dict,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    query_stmt = insert(AgentResponse).values(**insert_dict_).returning(AgentResponse)
    status, data = None, None
    try:
        with db.begin():
            status = db.execute(query_stmt)
            data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while inserting record AgentResponse, Error - {e}",
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully inserted AgentResponse id: {data.id}",
        )
    return data


def update_actions_info(db: Session, update_dict: dict, rules_id: int) -> Optional[AgentResponse]:
    update_dict_ = {**update_dict, "updated_at": datetime.now()}
    query_stmt = (
        update(AgentResponse).where(AgentResponse.id == rules_id).values(**update_dict_).returning(AgentResponse)
    )
    status, data = None, None
    try:
        with db.begin():
            status = db.execute(query_stmt)
            data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while updating AgentResponse, for id: {rules_id}, Error - {e}",
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully updated actions_info id: {data.id}",
        )
    return data
