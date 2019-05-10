from app.db.base_class import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    chart1_id = Column(Integer, ForeignKey('chart.id'), index=True)
    chart1 = relationship('Chart', backref='tasks')
    chart2_id = Column(Integer, ForeignKey('chart.id'), index=True)
    chart2 = relationship('Chart', backref='tasks')
    survey_id = Column(Integer, ForeignKey('survey.id'), index=True)
    survey = relationship('Survey', backref='tasks')
