from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from sqlalchemy_utils import TSVectorType

from app.db.base_class import Base
from app.db.utils import ArrayOfEnum
from app.models.chart import ChartType


class Chart(Base):
    id = Column(Integer, primary_key=True, index=True)
    file_hash = Column(String(64))
    file_ext = Column(String(10))
    type = Column(ArrayOfEnum(Enum(ChartType)), index=True)
    title = Column(String(200), index=True)
    x_axis_title = Column(String(200), index=True)
    y_axis_title = Column(String(200), index=True)
    description = Column(String(4000), index=True)
    search_vector = Column(
        TSVectorType('title', 'x_axis_title', 'y_axis_title', 'description'))
    created = Column(DateTime, server_default=func.now())
