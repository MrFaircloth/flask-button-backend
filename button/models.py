from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SaveEvent(Base):
    __tablename__ = 'save_events'

    id = Column(String, primary_key=True)
    name = Column(String)
    last_saved = Column(DateTime)
    interval = Column(Integer)
    time_left = Column(Integer)  # Using Integer column for time_left in seconds
    saves_count = Column(Integer)


class ButtonState(Base):
    __tablename__ = 'button_state'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    completion_date = Column(DateTime)
    delta_times = Column(JSON, nullable=False)
    interval_times = Column(JSON)