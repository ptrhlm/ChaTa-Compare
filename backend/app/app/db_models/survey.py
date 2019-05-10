from app.db.base_class import Base
from app.enums.survey_status import SurveyStatus
from app.enums.survey_type import SurveyType
from sqlalchemy import Boolean, Column, Integer, String, Enum, Float, ForeignKey
from sqlalchemy.orm import relationship

from .chart_survey_association import chart_survey_association
from .survey_user_association import survey_user_association


class Survey(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    description = Column(String(4000))
    status = Column(Enum(SurveyStatus), index=True, default=SurveyStatus.OPEN)
    type = Column(Enum(SurveyType), index=True)
    charts = relationship('Chart', secondary=chart_survey_association, backref='surveys')
    researcher_id = Column(Integer, ForeignKey('user.id'), index=True)
    researcher = relationship('User', backref='created_surveys')
    participants = relationship('User', secondary=survey_user_association, backref='participated_surveys')
    answers_per_task = Column(Integer)
    tasks_per_chart = Column(Integer)
    exp_required = Column(Boolean, default=False)
    min_answers_quality = Column(Float, default=0.0)
