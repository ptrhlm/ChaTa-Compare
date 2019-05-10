from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Criterion(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    survey_id = Column(Integer, ForeignKey('survey.id'), index=True)
    survey = relationship('Survey', backref='criteria')
