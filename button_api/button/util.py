from datetime import datetime, timedelta
from typing import List
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


def get_future_timestamp(time_delta: timedelta, start: datetime = None) -> datetime:
    start = datetime.now() if not start else start
    future_datetime = start + time_delta  #  + random_delta
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
    if not query_results:
        return []

    def convert(model):
        model_dict: dict = model.__dict__
        model_dict.pop('_sa_instance_state')
        return model_dict

    if not isinstance(query_results, list):
        return [convert(query_results)]

    return [convert(model) for model in query_results]


def create_deltas(
    total_time: timedelta, deviation: timedelta, chunks: int
) -> List[timedelta]:
    '''
    Creates a list of timedeltas which in order equal the total_time. The length of the list will be equal to the chunks.
    The values will not be unifrom as they will slightly deviate.
    For example:
        total_time=timedelta(hours=1, minutes=30), deviation=timedelta(minutes=10), chunks=3
        returns ( timedelta(minutes=23), timedelta(minutes=40), timedelta(minutes=27))

    The sum of the deltas will equal total_time (1 hour and 30 minutes),
    the length of the list is chunks (3)
    and they all deviate from the average by a maximum of deviation (10 minutes).
    '''
    average_time = total_time / chunks

    intervals = []
    remaining_time = total_time

    for _ in range(chunks - 1):
        max_deviation_seconds = deviation.total_seconds()
        deviation_seconds = random.uniform(
            -max_deviation_seconds, max_deviation_seconds
        )

        # Cap the deviation to the specified maximum
        deviation_seconds = min(deviation_seconds, max_deviation_seconds)

        deviation_interval = timedelta(seconds=deviation_seconds)

        interval = average_time + deviation_interval
        intervals.append(interval)

        remaining_time -= interval

    intervals.append(remaining_time)

    return intervals


def create_intervals(start_time: datetime, deltas: List[timedelta]) -> List[datetime]:
    '''
    Using a list of time deltas, creates a list of datetimes from the specified starting point.
    '''
    result = []
    current_time = start_time
    for delta in deltas:
        current_time += delta
        result.append(current_time)
    return result
