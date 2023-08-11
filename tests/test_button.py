import pytest
from datetime import datetime, timedelta
from button_api.button.button_manager import Button


@pytest.fixture
def button() -> Button:
    return Button(total_time="1h", total_life_time="10m", deviation_time='5m', interval_chunks=3)

def test_remove_expired_intervals():
    intervals = [
        datetime.now() - timedelta(hours=1),
        datetime.now() - timedelta(minutes=30),
        datetime.now() + timedelta(minutes=15),
        datetime.now() + timedelta(hours=2),
    ]
    cutoff = datetime.now() - timedelta(minutes=45)

    remaining_intervals = Button._remove_expired_intervals(intervals, cutoff)
    assert len(remaining_intervals) == 2
    assert all(dt >= cutoff for dt in remaining_intervals)
    assert all(dt in intervals for dt in remaining_intervals)