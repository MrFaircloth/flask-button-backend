import pytest
from datetime import timedelta
from button.button import Button


@pytest.fixture
def button() -> Button:
    return Button(total_time="1h", interval_time="10m", interval_chunks=3)


def test_button_initial_state(button: Button):
    status_details = button.get_status()
    assert status_details['current_interval'] == 3
    assert status_details['alive'] is True
    assert status_details['complete'] is False
    assert status_details['interval_count'] == 3


def test_button_interval_advancement(button: Button):
    one_minute = timedelta(minutes=1)
    comparison_datetime = button._init_date + button._interval_time + one_minute

    status_details = button.get_status(comparison_datetime)
    assert status_details['current_interval'] == 2
    assert status_details['alive'] is True
    assert status_details['complete'] is False
    assert status_details['interval_count'] == 3


def test_button_completion():
    button = Button(total_time="10", interval_time="10m", interval_chunks=3)
    interval_jump = timedelta(minutes=11)
    comparison_datetime = button._init_date + interval_jump
    status_details = button.get_status(comparison_datetime)

    assert status_details['current_interval'] == 0
    assert status_details['alive'] is True
    assert status_details['complete'] is True
    assert status_details['interval_count'] == 3


def test_button_reset(button: Button):
    one_minute = timedelta(minutes=1)
    comparison_datetime = button._init_date + button._interval_time + one_minute

    status_details = button.get_status(comparison_datetime)
    assert status_details['current_interval'] == 2
    assert status_details['alive'] is True
    assert status_details['complete'] is False
    assert status_details['interval_count'] == 3

    button.reset()

    status_details = button.get_status()
    assert status_details['current_interval'] == 3
    assert status_details['alive'] is True
    assert status_details['complete'] is False
    assert status_details['interval_count'] == 3
