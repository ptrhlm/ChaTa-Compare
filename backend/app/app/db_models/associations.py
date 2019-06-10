from sqlalchemy import Column, Integer, Table, ForeignKey, Float
import trueskill

from app.db.base_class import Base


chart_survey_association = Table('chart_survey_association', Base.metadata,
                                 Column('chart_id', Integer, ForeignKey('chart.id')),
                                 Column('survey_id', Integer, ForeignKey('survey.id')),
                                 Column('sigma', Float, default=trueskill.SIGMA),
                                 Column('mu', Float, default=trueskill.MU))

survey_user_association = Table('survey_user_association', Base.metadata,
                                Column('survey_id', Integer, ForeignKey('survey.id')),
                                Column('user_id', Integer, ForeignKey('user.id')))
