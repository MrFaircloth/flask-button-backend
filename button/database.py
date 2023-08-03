from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Replace 'sqlite:///button_data.db' with the desired SQLite database path
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///button_data.db')

Base = declarative_base()

class ButtonData(Base):
    __tablename__ = 'button_data'

    id = Column(String, primary_key=True)
    name = Column(String)
    last_saved = Column(DateTime)
    interval = Column(Integer)
    time_left = Column(Integer)  # Using Integer column for time_left in seconds
    saves_count = Column(Integer)

def create_database_if_not_exists():
    if not os.path.exists('button_data.db'):
        create_database()

def create_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

def upsert_data(data):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    existing_data = session.query(ButtonData).filter(ButtonData.id == data['id']).first()
    if existing_data:
        # Update existing record
        existing_data.name = data['name']
        existing_data.last_saved = data['last_saved']
        existing_data.interval = data['interval']
        existing_data.time_left = data['time_left']
        existing_data.saves_count += 1 # Increase saves_count by one with every upsert
    else:
        # Insert new record
        data['saves_count'] = 0
        new_data = ButtonData(**data)
        session.add(new_data)

    session.commit()
    session.close()

def query_by_id(id):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    data = session.query(ButtonData).filter(ButtonData.id == id).first()
    session.close()

    return data

def query_least_time_left():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query the record with the least time_left value
    least_time_left_data = session.query(ButtonData).order_by(ButtonData.time_left.asc()).first()
    session.close()

    return least_time_left_data

if __name__ == '__main__':
    create_database_if_not_exists()
