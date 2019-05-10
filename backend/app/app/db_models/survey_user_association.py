from app.db.base_class import Base
from sqlalchemy import Column, Integer, Table, ForeignKey

survey_user_association = Table('survey_user_association', Base.metadata,
                                Column('survey_id', Integer, ForeignKey('survey.id')),
                                Column('user_id', Integer, ForeignKey('user.id')))
