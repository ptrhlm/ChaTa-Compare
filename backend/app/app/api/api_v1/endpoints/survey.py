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


@router.post("/surveys")
def create_survey(body = ...):
    pass


@router.delete("/surveys/{id}/charts/{chart_id}")
def remove_chart(survey_id, id):
    pass


@router.get("/surveys")
def list_surveys():
    pass


@router.put("/surveys/{id}/close")
def close_survey():
    pass


@router.post("/surveys/{id}/participants")
def add_participant():
    pass
