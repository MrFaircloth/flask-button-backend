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
    # Calculate the time difference between the two datetimes
    time_difference = end_time - start_time

    # Convert the time difference to total seconds
    total_seconds = int(time_difference.total_seconds())

    # Calculate the components (days, hours, minutes, seconds)
    days = time_difference.days
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Build the human-readable string
    result = ""
    if days > 0:
        result += f"{days} days"
    if hours > 0:
        result += f", {hours} hours"
    if minutes > 0:
        result += f", {minutes} minutes"
    if seconds > 0 and days == 0 and hours == 0 and minutes == 0:
        result += f", {seconds} seconds"

    return result.strip(', ')
