from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Answer(Base):
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('task.id'), index=True)
    task = relationship('Task', backref='answers')
    chosen_chart_id = Column(Integer, ForeignKey('chart.id'), index=True)
    chosen_chart = relationship('Chart', backref='answers')
    score = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    user = relationship('User', backref='answers')
    created = Column(DateTime, server_default=func.now())
