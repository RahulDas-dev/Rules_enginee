import logging
from typing import Mapping

from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.orm import Session

from src.db.provider import get_db_session

# from src.endpoints.scores.schemas import ProjectBody

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/calculate/", status_code=status.HTTP_201_CREATED)
def calcuate_score(file: UploadFile, session: Session = Depends(get_db_session)) -> Mapping[str, str]:
    logger.info(f"Session id: {id(session)} | filename: {file.filename} ")
    return {"filename": file.filename}
