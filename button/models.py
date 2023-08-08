from sqlalchemy import Column, String, Integer, DateTime
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

    id = Column(String, primary_key=True)
    name = Column(String)
    last_saved = Column(DateTime)
    interval = Column(Integer)
    time_left = Column(Integer)  # Using Integer column for time_left in seconds
    saves_count = Column(Integer)