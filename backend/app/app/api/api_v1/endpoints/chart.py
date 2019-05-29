import logging
import os
from typing import List

import aiofiles
import ujson
from fastapi import Depends, File, HTTPException, Path, UploadFile, APIRouter
from starlette.responses import FileResponse

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import (get_current_active_researcher,
                                    get_current_active_user)
from app.core import config
from app.db.session import Session
from app.db_models.chart import Chart
from app.db_models.user import User as DBUser
from app.models.chart import ChartBase, ChartInCreate, ChartType

router = APIRouter()


@router.get("/charts/{chart_id}", tags=["charts"])
async def get_chart(
        *,
        chart_id: int = Path(..., title="The ID of the chart to get"),
        db: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_active_user),
):
    """Get one chart"""
    chart = crud.chart.get(db, chart_id=chart_id)
    if not chart:
        raise HTTPException(
            status_code=404,
            detail="Chart not found.",
        )
    else:
        return FileResponse(chart.filepath)


@router.get("/charts/", tags=["charts"], response_model=List[int])
def search_charts(
        db: Session = Depends(get_db),
        q: str = None,
        current_user: DBUser = Depends(get_current_active_researcher),
):
    """Search charts"""
    charts = crud.chart.search(db, q=q)
    return [chart.id for chart in charts]


@router.post("/charts/", tags=["charts"], response_model=List[int])
async def create_charts(
        *,
        db: Session = Depends(get_db),
        files: List[UploadFile] = File(...),
        current_user: DBUser = Depends(get_current_active_researcher),
):
    """Create multiple charts and store their images"""
    logging.info('Saving charts - start')
    if not current_user:  # dead code: remove
        raise HTTPException(
            status_code=400,
            detail="The user is not authorized to upload charts.",
        )
    charts_json_file, charts = next(file for file in files if file.filename == "charts.json"), \
                               [file for file in files if not file.filename == "charts.json"]
    json_content = await charts_json_file.read()
    parsed_json = ujson.loads(json_content)
    for chart in parsed_json:
        chart['type'] = ChartType(str(chart['type']).lower())

    logging.info('Saving charts')

    charts_in = [ChartInCreate.parse_obj(chart_json) for chart_json in parsed_json]
    charts_in_db = [None] * len(charts_in)
    curpath = os.path.abspath(os.curdir)
    os.makedirs(config.CHARTS_DIRECTORY, exist_ok=True)
    for idx, chart in enumerate(charts_in):
        path = os.path.join(curpath, config.CHARTS_DIRECTORY, chart.file_name)
        async with aiofiles.open(path, 'wb') as saved_chart:
            chart_file = next(file for file in files if file.filename == chart.file_name)
            await saved_chart.write(chart_file.file.read())
            charts_in_db[idx] = Chart(filepath=path,
                                      type=chart.type,
                                      title=chart.title,
                                      x_axis_title=chart.x_axis_title,
                                      y_axis_title=chart.y_axis_title,
                                      description=chart.description)
    created_charts = crud.chart.create(db, charts_in=charts_in_db)
    return [chart.id for chart in created_charts]


@router.delete("/charts/{id}", tags=["charts"])
async def delete_chart(
        id: int,
        db: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_active_user)
):
    """Remove chart if not used in any survey"""
    raise NotImplementedError()  # TODO: later
