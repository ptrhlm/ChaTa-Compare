from app.db.base_class import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Answer(Base):
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('task.id'), index=True)
    task = relationship('Task', backref='answers')
    criterion_id = Column(Integer, ForeignKey('criterion.id'), index=True)
    criterion = relationship('Criterion', backref='answers')
    score = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    user = relationship('User', backref='answers')
