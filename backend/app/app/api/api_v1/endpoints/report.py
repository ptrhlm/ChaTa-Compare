from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser, get_current_active_user
from app.core import config
from app.db_models.user import User as DBUser
from app.models.user import User, UserInCreate, UserInDB, UserInUpdate
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/surveys/{id}/summary")
def survey_summary():
    pass


@router.get("/surveys/{id}/report")
def survey_report():
    pass
