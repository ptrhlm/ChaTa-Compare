from typing import List, Optional

from app.db_models.chart import Chart
from sqlalchemy_searchable import search as db_search


def create(db_session, *, charts_in: List[Chart]) -> List[Chart]:
    db_session.add_all(charts_in)
    db_session.commit()
    for chart in charts_in:
        db_session.refresh(chart)
    return charts_in


def search(db_session, *, q: str) -> List[Chart]:
    query = db_session.query(Chart)
    query = db_search(query, q, sort=True)
    return query


def get(db_session, *, chart_id: int) -> Optional[Chart]:
    return db_session.query(Chart).filter(Chart.id == chart_id).first()
