from app.db.base_class import Base
from app.models.chart import ChartType
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy_utils import TSVectorType


class Chart(Base):
    id = Column(Integer, primary_key=True, index=True)
    file_hash = Column(String(64))
    file_ext = Column(String(10))
    type = Column(Enum(ChartType), index=True)
    title = Column(String(200), index=True)
    x_axis_title = Column(String(200), index=True)
    y_axis_title = Column(String(200), index=True)
    description = Column(String(4000), index=True)
    search_vector = Column(TSVectorType('title', 'x_axis_title', 'y_axis_title', 'description'))
