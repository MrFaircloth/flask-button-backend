from datetime import datetime, timedelta
import random


def parse_time_string(time_str: str) -> timedelta:
    # Parse a time string of the format "XdYhZmWs" where X is days, Y is hours, Z is minutes, and W is seconds.
    days, time_str = time_str.split("d") if "d" in time_str else (0, time_str)
    hours, time_str = time_str.split("h") if "h" in time_str else (0, time_str)
    minutes, time_str = time_str.split("m") if "m" in time_str else (0, time_str)
    seconds, _ = time_str.split("s") if "s" in time_str else (0, time_str)

    return timedelta(
        days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds)
    )


def get_future_timestamp(
    time_delta: timedelta, start: datetime = None
) -> datetime:
    start = datetime.now() if not start else start
    future_datetime = start + time_delta #  + random_delta
    return future_datetime


def get_time_difference(start_time: datetime, end_time: datetime) -> str:
    time_difference = end_time - start_time
    total_seconds = int(time_difference.total_seconds())
    
    days = time_difference.days
    hours = total_seconds // 3600 % 24
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    result = ""
    if days > 0:
        result += f"{days} days"
    if hours > 0:
        result += f", {hours} hours"
    if minutes > 0:
        result += f", {minutes} minutes"
    if seconds > 0:
        result += f", {seconds} seconds"
    
    return result.strip(', ')


def results_to_dict(query_results) -> dict:
    '''
    [{
        "interval": 20,
        "name": "Mitch",
        "saves_count": 1,
        "time_left": 215938,
        "last_saved": datetime.datetime(2023, 8, 4, 12, 17, 30, 602022),
        "id": "26159207"
    }]
    '''
    if not isinstance(query_results, list): query_results = [ query_results ]
    data = [item.__dict__ for item in query_results]
    # Remove the "_sa_instance_state" key from each dictionary
    data = [{k: v for k, v in item.items() if k != '_sa_instance_state'} for item in data]
    return data