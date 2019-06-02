import base64
import hashlib
import io
import logging
import os
import os.path
from typing import List

from app import crud
from app import models
from app.api.utils.db import get_db
from app.api.utils.security import (get_current_active_researcher,
                                    get_current_active_user)
from app.api.utils.storage import get_storage
from app.core import config
from app.db.session import Session
from app.db_models.user import User as DBUser
from app.models.chart import ChartBase, ChartInCreate, Chart, ChartInDB
from app.storage import get_url
from fastapi import Depends, HTTPException, Path, APIRouter
from minio import Minio

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/charts/{chart_id}", tags=["charts"], response_model=Chart)
async def get_chart(*,
                    chart_id: int = Path(...,
                                         title="The ID of the chart to get"),
                    db: Session = Depends(get_db),
                    current_user: DBUser = Depends(get_current_active_user)):
    """Get one chart"""
    db_chart = crud.chart.get(db, chart_id=chart_id)
    if not db_chart:
        raise HTTPException(
            status_code=404,
            detail="Chart not found.",
        )
    else:
        chart = models.chart.Chart(type=db_chart.type,
                                   title=db_chart.title,
                                   x_axis_title=db_chart.x_axis_title,
                                   y_axis_title=db_chart.y_axis_title,
                                   description=db_chart.description,
                                   )
        chart.file_path = get_url(db_chart.file_hash + db_chart.file_ext)
        return chart


@router.get("/charts/search", tags=["charts"], response_model=List[Chart])
def search_charts(
        db: Session = Depends(get_db),
        q: str = None,
        current_user: DBUser = Depends(get_current_active_researcher),
):
    """Search charts"""
    charts = crud.chart.search(db, q=q)
    return charts


@router.post("/charts", tags=["charts"], response_model=List[models.chart.Chart])
async def create_chart(
        charts: List[ChartInCreate],
        *,
        db: Session = Depends(get_db),
        storage: Minio = Depends(get_storage),
        current_user: DBUser = Depends(get_current_active_researcher),
):
    """Create multiple charts and store their images"""

    charts_db = list()

    for chart in charts:
        file_ext = os.path.splitext(chart.file_name)[1]
        file_contents = base64.b64decode(chart.file_contents)
        m = hashlib.sha256()
        m.update(file_contents)
        file_hash = m.hexdigest()

        chart = chart.dict(exclude={'file_name', 'file_contents'})
        chart["file_ext"] = file_ext
        chart["file_hash"] = file_hash
        chart = ChartInDB(**chart)
        charts_db.append(chart)

        file_io = io.BytesIO(file_contents)
        try:
            storage.put_object(config.MINIO_BUCKET,
                               file_hash + file_ext,
                               file_io,
                               length=len(file_contents))
        except Exception as err:
            logger.error(err)
            raise HTTPException(status_code=500,
                                detail='Upload of chart failed')

    created_charts = crud.chart.create(db, charts_in=charts_db)
    response = []
    for created_chart in created_charts:
        chart = models.chart.Chart(
            type=created_chart.type,
            title=created_chart.title,
            x_axis_title=created_chart.x_axis_title,
            y_axis_title=created_chart.y_axis_title,
            description=created_chart.description,
            file_path=get_url(created_chart.file_hash + created_chart.file_ext),
        )
        response.append(chart)
    return response


@router.delete("/charts/{id}", tags=["charts"])
async def delete_chart(
        id: int,
        db: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_active_user)):
    """Remove chart if not used in any survey"""
    raise NotImplementedError()  # TODO: before the end of the world
