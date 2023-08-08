from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from button_manager import Button
from config import config
from models import SaveEvent, ButtonState, Base

# Replace 'sqlite:///button_data.db' with the desired SQLite database path
DATABASE_URL = config.DATABASE_URL


def create_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)


## SaveEvents

def upsert_data(data):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    existing_data = (
        session.query(SaveEvent).filter(SaveEvent.id == data['id']).first()
    )
    if existing_data:
        # Update existing record
        existing_data.name = data['name']
        existing_data.last_saved = data['last_saved']
        existing_data.interval = data['interval']
        existing_data.time_left = data['time_left']
        existing_data.saves_count += 1  # Increase saves_count by one with every upsert
    else:
        # Insert new record
        data['saves_count'] = 1
        new_data = SaveEvent(**data)
        session.add(new_data)

    session.commit()
    session.close()


def query_by_id(id):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = session.query(SaveEvent).filter(SaveEvent.id == id).first()
    session.close()

    return data


def query_get_leaderboard():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query the record with the least time_left value
    least_time_left_data = (
        session.query(SaveEvent).order_by(SaveEvent.time_left.asc()).all()
    )
    session.close()

    return least_time_left_data

## ButtonState

def insert_button_state(button: Button):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    new_button_state = ButtonState(
        timestamp=datetime.now(),
        creation_date=button._init_date,
        completion_date=button._complete_date,
        delta_times=button._delta_times,
        interval_times=button._interval_times
    )
    session.add(new_button_state)
    session.commit()
