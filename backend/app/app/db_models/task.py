from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    chart1_id = Column(Integer, ForeignKey('chart.id'), index=True)
    chart1 = relationship('Chart', backref='tasks_chart_1', foreign_keys=[chart1_id])
    chart2_id = Column(Integer, ForeignKey('chart.id'), index=True)
    chart2 = relationship('Chart', backref='tasks', foreign_keys=[chart2_id])
    survey_id = Column(Integer, ForeignKey('survey.id'), index=True)
    survey = relationship('Survey', backref='tasks_chart_2')
    created = Column(DateTime, server_default=func.now())
