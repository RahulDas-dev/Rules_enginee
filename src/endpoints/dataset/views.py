import logging
from typing import Mapping

from fastapi import APIRouter, Depends, UploadFile, status
from genson import SchemaBuilder
from sqlalchemy.orm import Session

from src.core.dataloader import XmlLoader
from src.core.transformer import RemovePrefix
from src.db.curd.data_model import insert_data_model
from src.db.curd.dataset import insert_datasets
from src.db.provider import get_db_session

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/new/", status_code=status.HTTP_201_CREATED)
def new(version: str, file: UploadFile, session: Session = Depends(get_db_session)) -> Mapping[str, str]:
    logger.info(f"Session id: {id(session)} | filename: {file.filename} ")
    try:
        file_content = file.file.read()
        loder = XmlLoader.from_content(file_content.decode("utf-8"))
        documents = RemovePrefix().transform(loder.document)
        # json_data = json.dumps(documents, indent=4)
    except Exception as e:
        logger.error(f"Error while loading data: {e}")
        documents = {}
        message = "Error while loading Dataset"
    else:
        metadata = {
            "name": file.filename,
            "extn": file.filename.split(".")[-1],
        }
        inser_dict = {
            "version": version,
            "dmetadata": metadata,
            "dformat": file.filename.split(".")[-1],
            "data": documents,
        }
        insert_datasets(session, inser_dict)
        message = "Dataset created successfully"
    return {"message": message}


@router.post("/build_schema/", status_code=status.HTTP_201_CREATED)
def add_dataschema(version: str, file: UploadFile, session: Session = Depends(get_db_session)) -> Mapping[str, str]:
    logger.info(f"Session id: {id(session)} | filename: {file.filename} ")
    try:
        file_content = file.file.read()
        loder = XmlLoader.from_content(file_content.decode("utf-8"))
        documents = RemovePrefix().transform(loder.document)
        builder = SchemaBuilder()
        builder.add_object(documents)

        # Generate schema from the dictionary
        schema = builder.to_schema()
    except Exception as e:
        logger.error(f"Error while loading data: {e}")
        schema = {}
        message = "Error while Schema Creation"
    else:
        inser_dict = {"version": version, "schema": schema}
        insert_data_model(session, inser_dict)
        message = "Data Schema Created successfully"
    return {"message": message}
