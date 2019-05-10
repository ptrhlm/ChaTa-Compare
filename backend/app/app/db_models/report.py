from app.db.base_class import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Report(Base):
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('task.id'), index=True)
    task = relationship('Task', backref='reports')
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    user = relationship('User', backref='reports')
