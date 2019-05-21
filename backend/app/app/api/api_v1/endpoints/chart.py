from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser, get_current_active_user
from app.core import config
from app.db_models.user import User
from app.models.chart import ChartType, Chart

router = APIRouter()


@router.get("/charts", tags=["charts"], response_model=List[Chart])
async def list_charts(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """List charts"""
    charts = crud.chart.get_multi(db, skip=skip, limit=limit)
    return charts

@router.get("/charts/search", tags=["charts"], response_model=List[Chart])
async def search(
        text: str,
        type: Optional[ChartType] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Search for charts"""
    charts = crud.chart.search(db, text=text, type=type, skip=skip, limit=limit)
    return charts

@router.get("/charts/{id}", tags=["charts"], response_model=Chart)
async def get_chart(
        id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get one chart"""
    chart = crud.chart.get_one(db, id=id)
    return chart


@router.post("/charts", tags=["charts"])
async def add_charts(
        charts: List[Chart],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Add charts to database"""
    crud.chart.create_multi(db, charts=charts, user=current_user)


@router.delete("/charts/{id}", tags=["charts"])
async def delete_chart(
        id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Remove chart if not used in any survey"""
    raise NotImplementedError()  # TODO
