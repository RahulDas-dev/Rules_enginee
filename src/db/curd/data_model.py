import logging
from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from src.db.orms import DataModel

logger = logging.getLogger(__name__)


def get_data_model(db: Session, data_id: int) -> Optional[DataModel]:
    query_stmt = select(DataModel).where(DataModel.id == data_id)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching DataModel, for id: {data_id}, Error - {e}",
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched DataModel details for id: {data_id}",
        )
    return data


def get_data_model_by_version(db: Session, version: str) -> Optional[DataModel]:
    query_stmt = select(DataModel).where(DataModel.version == version)
    status, data = None, []
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching DataModel, for version: {version}, Error - {e}",
        )
        data = []
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched DataModel for version : {version}",
        )
    return data


def get_latest_data_model(db: Session) -> Sequence[DataModel]:
    query_stmt = select(DataModel).order_by(DataModel.created_at.desc()).limit(1)
    status, data = None, []
    try:
        status = db.execute(query_stmt)
        data = status.scalars().all()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching DataModel, Error - {e}",
        )
        data = []
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched latest DataModel",
        )
    return data


def insert_data_model(db: Session, insert_dict: dict) -> Optional[DataModel]:
    insert_dict_ = {
        **insert_dict,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    query_stmt = insert(DataModel).values(**insert_dict_).returning(DataModel)
    status, data = None, None
    try:
        with db.begin():
            status = db.execute(query_stmt)
            data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while inserting record DataModel, Error - {e}",
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully inserted DataModel id: {data.id}",
        )
    return data


def update_dataset(
    db: Session,
    update_dict: dict,
    data_id: int,
) -> Optional[DataModel]:
    update_dict_ = {**update_dict, "updated_at": datetime.now()}
    query_stmt = update(DataModel).where(DataModel.id == data_id).values(**update_dict_).returning(DataModel)
    status, data = None, None
    try:
        with db.begin():
            status = db.execute(query_stmt)
            data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while updating DataModel, for id: {data_id}, Error - {e}",
        )
        data = None
    else:
        logger.info(f"Session id {id(db)} | Sucessfully updated DataModel id: {data.id}")
    return data
