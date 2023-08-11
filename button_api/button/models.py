from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SaveEvent(Base):
    __tablename__ = 'save_events'

    id = Column(
        String(50), primary_key=True
    )  # Limiting the length of the String column
    name = Column(String(255))  # Limiting the length of the String column
    last_saved = Column(TIMESTAMP)
    interval = Column(Integer)
    time_left = Column(Integer)  # Using Integer column for time_left in seconds
    saves_count = Column(Integer)


class ButtonState(Base):
    __tablename__ = 'button_state'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    creation_date = Column(TIMESTAMP, nullable=False)
    completion_date = Column(TIMESTAMP, nullable=False)
    delta_times = Column(JSON, nullable=False)
    interval_times = Column(JSON, nullable=False)
