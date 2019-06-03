from app.db.base_class import Base
from sqlalchemy import Column, Integer, Table, ForeignKey

chart_survey_association = Table('chart_survey_association', Base.metadata,
                                 Column('chart_id', Integer, ForeignKey('chart.id')),
                                 Column('survey_id', Integer, ForeignKey('survey.id')))

survey_user_association = Table('survey_user_association', Base.metadata,
                                Column('survey_id', Integer, ForeignKey('survey.id')),
                                Column('user_id', Integer, ForeignKey('user.id')))
