from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from datetime import datetime
import logging
import os

from .button_manager import Button
from .config import config
from .models import SaveEvent, ButtonState, Base

# Replace 'sqlite:///button_data.db' with the desired SQLite database path
DATABASE_URL: str = config.DATABASE_URL if config else 'sqlite:///button_data.db'


def get_engine() -> Engine:
    '''
    Creates engine - adding user credentials if available
    '''
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    database_url = DATABASE_URL

    if username and password:
        # Insert username and password into the DATABASE_URL string
        credentials = f'{username}:{password}'
        database_url = database_url.replace('://', f'://{credentials}')

    engine = create_engine(database_url)
    return engine


def create_database():
    logging.info('Creating database tables if not already existing.')
    engine = get_engine()
    Base.metadata.create_all(engine)


def get_session() -> Session:
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


## SaveEvents


def upsert_data(data: dict):
    logging.debug('Upserting SaveEvent data.')
    with get_session() as session:
        existing_data = (
            session.query(SaveEvent).filter(SaveEvent.id == data['id']).first()
        )
        if existing_data:
            # Update existing record
            existing_data.name = data['name']
            existing_data.last_saved = data['last_saved']
            existing_data.interval = data['interval']
            existing_data.time_left = data['time_left']
            existing_data.saves_count += (
                1  # Increase saves_count by one with every upsert
            )
        else:
            # Insert new record
            data['saves_count'] = 1
            new_data = SaveEvent(**data)
            session.add(new_data)

        session.commit()

def query_by_id(id):
    logging.debug(f"Collecting user {id}'s SaveEvent.")
    with get_session() as session:
        data = session.query(SaveEvent).filter(SaveEvent.id == id).first()
        return data


def query_get_leaderboard():
    logging.debug('Collecting user scores.')
    with get_session() as session:
        # Query the record with the least time_left value
        least_time_left_data = (
            session.query(SaveEvent).order_by(SaveEvent.time_left.desc()).all()
        )
        session.close()
        return least_time_left_data


## ButtonState


def insert_button_state(button: Button):
    logging.info('Saving button current state.')
    interval_time_deltas_seconds = [
        delta.total_seconds() for delta in button._interval_time_deltas
    ]
    interval_times_epoch_seconds = [dt.isoformat() for dt in button._interval_times]

    with get_session() as session:
        new_button_state = ButtonState(
            timestamp=datetime.now().isoformat(),
            creation_date=button._creation_date.isoformat(),
            completion_date=button._completion_date.isoformat(),
            delta_times=interval_time_deltas_seconds,
            interval_times=interval_times_epoch_seconds,
        )
        session.add(new_button_state)
        session.commit()
    logging.info('Button state saved successfully.')


def get_latest_state():
    logging.info('Fetching latest button state.')
    with get_session() as session:
        # Query the record with the least time_left value
        latest_button = (
            session.query(ButtonState).order_by(ButtonState.timestamp).limit(1).first()
        )
        session.close()

        return latest_button
