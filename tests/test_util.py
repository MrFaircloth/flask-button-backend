import pytest
import random
from datetime import datetime, timedelta
from button_api.button.util import (
    get_time_difference,
    parse_time_string,
    get_future_timestamp,
    create_deltas,
    create_intervals,
)


@pytest.mark.parametrize(
    "start_time, end_time, expected_result",
    [
        (
            datetime(2023, 8, 1, 10, 0, 0),
            datetime(2023, 8, 1, 12, 30, 0),
            "2 hours, 30 minutes",
        ),
        (
            datetime(2023, 8, 1, 10, 0, 0),
            datetime(2023, 8, 2, 14, 30, 0),
            "1 days, 4 hours, 30 minutes",
        ),
        (
            datetime(2023, 8, 1, 10, 0, 0),
            datetime(2023, 8, 4, 15, 30, 45),
            "3 days, 5 hours, 30 minutes, 45 seconds",
        ),
    ],
)
def test_get_time_difference(start_time, end_time, expected_result):
    result = get_time_difference(start_time, end_time)
    assert result == expected_result


# Test cases for parse_time_string
def test_parse_time_string():
    assert parse_time_string("2d3h15m30s") == timedelta(
        days=2, hours=3, minutes=15, seconds=30
    )
    assert parse_time_string("1h30s") == timedelta(hours=1, seconds=30)
    assert parse_time_string("5m") == timedelta(minutes=5)
    assert parse_time_string("120s") == timedelta(seconds=120)
    assert parse_time_string("3d10h") == timedelta(days=3, hours=10)
    assert parse_time_string("1d2h5m") == timedelta(days=1, hours=2, minutes=5)


# Test cases for get_future_timestamp
def test_get_future_timestamp():
    base_time = datetime(2023, 8, 1, 10, 0, 0)

    future_time = get_future_timestamp(timedelta(days=2, hours=5), base_time)
    assert future_time == datetime(2023, 8, 3, 15, 0, 0)

    future_time = get_future_timestamp(timedelta(hours=1, minutes=30), base_time)
    assert future_time == datetime(2023, 8, 1, 11, 30, 0)

    # Random timedelta
    random_time_delta = timedelta(
        days=random.randint(1, 10),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    future_time = get_future_timestamp(random_time_delta, base_time)
    assert future_time == base_time + random_time_delta


@pytest.mark.parametrize(
    "total_time, deviation, chunks",
    [
        (timedelta(hours=1, minutes=30), timedelta(minutes=10), 3),
        (timedelta(seconds=180), timedelta(seconds=20), 5),
        (timedelta(minutes=75), timedelta(minutes=5), 4),
        (timedelta(hours=3), timedelta(minutes=30), 6),
        # Add more parameter sets here
    ],
)
def test_create_deltas(total_time, deviation, chunks):
    deltas = create_deltas(total_time, deviation, chunks)

    assert sum(deltas, timedelta()) == total_time
    assert len(deltas) == chunks


def test_create_intervals():
    start_time = datetime(2023, 8, 1, 12, 0, 0)
    deltas = [timedelta(hours=1), timedelta(minutes=30), timedelta(seconds=45)]
    expected = [
        datetime(2023, 8, 1, 13, 0, 0),
        datetime(2023, 8, 1, 13, 30, 0),
        datetime(2023, 8, 1, 13, 30, 45),
    ]

    assert create_intervals(start_time, deltas) == expected

    # Edge case: empty list of deltas
    assert create_intervals(start_time, []) == []
