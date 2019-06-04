import base64
import hashlib
import io
import logging
import os
import os.path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path
from minio import Minio

from app import crud, models
from app.api.utils.db import get_db
from app.api.utils.security import (get_current_active_researcher,
                                    get_current_active_user)
from app.api.utils.storage import get_storage
from app.core import config
from app.db.session import Session
from app.db_models.user import User as DBUser
from app.models.chart import (Chart, ChartBase, ChartInCreate, ChartInDB,
                              ChartType, SearchParams)
from app.storage import get_url

router = APIRouter()
logger = logging.getLogger(__name__)


def db_chart_to_model_chart(db_chart):
    return models.chart.Chart(
        type=db_chart.type,
        title=db_chart.title,
        x_axis_title=db_chart.x_axis_title,
        y_axis_title=db_chart.y_axis_title,
        description=db_chart.description,
        file_path=get_url(db_chart.file_hash + db_chart.file_ext),
    )


@router.post("/charts/search", tags=["charts"], response_model=List[Chart])
def search_charts(
        db: Session = Depends(get_db),
        search_params: SearchParams = None,
        current_user: DBUser = Depends(get_current_active_researcher),
):
    """Search charts"""
    charts = crud.chart.search(db,
                               q=search_params.q,
                               chart_types=search_params.chart_types)
    return [db_chart_to_model_chart(chart) for chart in charts]


@router.post("/charts/search/ids", tags=["charts"], response_model=List[Chart])
def search_charts(
        db: Session = Depends(get_db),
        search_params: SearchParams = None,
        current_user: DBUser = Depends(get_current_active_researcher),
):
    """Search charts. Returns IDs"""
    charts = crud.chart.search(db,
                               q=search_params.q,
                               chart_types=search_params.chart_types)
    return [chart.id for chart in charts]


@router.get("/charts/{chart_id}", tags=["charts"], response_model=Chart)
async def get_chart(*,
                    chart_id: int = Path(...,
                                         title="The ID of the chart to get"),
                    db: Session = Depends(get_db),
                    storage: Minio = Depends(get_storage),
                    current_user: DBUser = Depends(get_current_active_user)):
    """Get one chart"""
    db_chart = crud.chart.get(db, chart_id=chart_id)
    if not db_chart:
        raise HTTPException(
            status_code=404,
            detail="Chart not found.",
        )
    else:
        return db_chart_to_model_chart(db_chart)


@router.post("/charts",
             tags=["charts"],
             response_model=List[models.chart.Chart])
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
        content_type = chart.mimetype

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
                               content_type=content_type,
                               length=len(file_contents))
        except Exception as err:
            logger.error(err)
            raise HTTPException(status_code=500,
                                detail='Upload of chart failed')

    created_charts = crud.chart.create(db, charts_in=charts_db)
    response = []
    for created_chart in created_charts:
        response.append(db_chart_to_model_chart(created_chart))
    return response


@router.delete("/charts/{id}", tags=["charts"])
async def delete_chart(
        id: int,
        db: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_active_user)):
    """Remove chart if not used in any survey"""
    raise NotImplementedError()  # TODO: before the end of the world
