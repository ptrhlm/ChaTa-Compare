from sqlalchemy import (Boolean, Column, DateTime, Enum, Float, ForeignKey,
                        Integer, String, func)
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db_models.associations import (chart_survey_association,
                                        survey_user_association)
from app.models.survey import SurveyStatus, SurveyType


class Survey(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    description = Column(String(4000))
    status = Column(Enum(SurveyStatus), index=True, default=SurveyStatus.OPEN)
    type = Column(Enum(SurveyType), index=True)
    created = Column(DateTime, server_default=func.now())
    deadline = Column(DateTime)
    charts = relationship('Chart',
                          secondary=chart_survey_association,
                          backref='surveys')
    researcher_id = Column(Integer, ForeignKey('user.id'), index=True)
    researcher = relationship('User', backref='created_surveys')
    participants = relationship('User',
                                secondary=survey_user_association,
                                backref='participated_surveys')
    answers_per_task = Column(Integer)
    tasks_per_chart = Column(Integer)
    exp_required = Column(Boolean, default=False)
    min_answers_quality = Column(Float, default=0.0)
