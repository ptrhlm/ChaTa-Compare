from typing import List, Optional

from app.db_models.chart import Chart
from app.models.chart import ChartInDB
from sqlalchemy_searchable import search as db_search


def create(db_session, *, charts_in: List[ChartInDB]) -> List[Chart]:
    charts = [Chart(
        file_hash=chart.file_hash,
        file_ext=chart.file_ext,
        type=chart.type,
        title=chart.title,
        x_axis_title=chart.x_axis_title,
        y_axis_title=chart.y_axis_title,
        description=chart.description,
    ) for chart in charts_in]
    db_session.add_all(charts)
    db_session.commit()
    for chart in charts:
        db_session.refresh(chart)
    return charts


def search(db_session, *, q: str) -> List[Chart]:
    query = db_session.query(Chart)
    query = db_search(query, q, sort=True)
    return query


def get(db_session, *, chart_id: int) -> Optional[Chart]:
    return db_session.query(Chart).filter(Chart.id == chart_id).first()
