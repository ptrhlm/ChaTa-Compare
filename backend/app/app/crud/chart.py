from typing import List, Optional

from app.db_models.chart import Chart
import app.models.chart as model
from app.db_models.user import User


async def get_multi(db_session, *, skip=0, limit=100) -> List[Optional[Chart]]:
    return db_session.query(Chart).offset(skip).limit(limit).all()


async def get_one(db_session, *, id: int) -> Optional[Chart]:
    return db_session.query(Chart).filter(Chart.id == id).first()


async def search(db_session,
                 *,
                 text: str,
                 type: Optional[model.ChartType],
                 skip: int = 0,
                 limit: int = 100) -> List[Optional[Chart]]:
    pass  # TODO


async def create_multi(db_session, *, charts: List[model.Chart],
                       user: User) -> None:
    pass  # TODO
