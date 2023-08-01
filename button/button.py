from datetime import datetime, timedelta
import random


class Button:
    '''
    Purpose: The Button was designed to function similar to a timer. The goal of the button is to remain 'alive' until it reaches its completion date.
    The timer length is determined by the provided interval and it will be broken up into chunks. These chunks give a rough estimate of how far along the button is. Once it reaches 0, the button's 'alive' status will be set to false and will become inoperable.
    The status of the button will only be known once checked. Upon checking, it report its alive status and it's current interval chunk along with any other relevant data.

    '''

    def __init__(
        self,
        total_time: str = "14d",
        interval_time: str = "3d",
        interval_chunks: int = 10,
        wiggle_time: str = '1h',
    ) -> None:
        self._init_date = datetime.now()

        self._total_time = self._parse_time_string(total_time)
        self._interval_time = self._parse_time_string(interval_time)
        self._interval_chunks = interval_chunks
        self._wiggle_time = wiggle_time

        self._alive = True
        self._complete_date = self._future_timestamp(self._total_time)
        self._current_interval = interval_chunks
        self._current_interval_end = self._future_timestamp(self._interval_time)

    def _parse_time_string(self, time_str: str) -> timedelta:
        # Parse a time string of the format "XdYhZmWs" where X is days, Y is hours, Z is minutes, and W is seconds.
        days, time_str = time_str.split("d") if "d" in time_str else (0, time_str)
        hours, time_str = time_str.split("h") if "h" in time_str else (0, time_str)
        minutes, time_str = time_str.split("m") if "m" in time_str else (0, time_str)
        seconds, _ = time_str.split("s") if "s" in time_str else (0, time_str)

        return timedelta(
            days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds)
        )

    def _future_timestamp(self, time_delta: timedelta, wiggle: str = "0s") -> datetime:
        wiggle_time = self._parse_time_string(wiggle)
        now = datetime.now()
        random_delta = timedelta(
            hours=random.randint(
                -wiggle_time.seconds // 3600, wiggle_time.seconds // 3600
            ),
            minutes=random.randint(
                -wiggle_time.seconds % 3600 // 60, wiggle_time.seconds % 3600 // 60
            ),
            seconds=random.randint(-wiggle_time.seconds % 60, wiggle_time.seconds % 60),
        )
        future_datetime = now + time_delta + random_delta
        return future_datetime

    def _is_complete(self) -> bool:
        '''
        If past the determined end time and still living, returns True
        '''
        now = datetime.now()
        return now > self._complete_date and self._alive

    def reset(self) -> None:
        '''
        Resets the button intervals. Setting the current interval to the maximum and setting the future timestamp to the interval hour setting.
        '''
        self._current_interval = self._interval_chunks
        self._current_interval_end = self._future_timestamp(
            self._interval_time, self._wiggle_time
        )

    def _advance_interval(self) -> None:
        '''
        Advances the button interval by one and updates next interval end.
        '''
        self._current_interval -= 1
        self._current_interval_end = self._future_timestamp(
            self._interval_time, self._wiggle_time
        )

    def get_current_interval(self, comparison: datetime = datetime.now()) -> int:
        '''
        Get's the current interval and advances if time is past due.
        '''

        if comparison > self._current_interval_end:
            self._advance_interval()

        return self._current_interval

    def get_status(self, comparison: datetime = datetime.now()) -> dict:
        '''
        Obtains and returns button status.
        '''
        complete = self._is_complete()
        interval = 0
        if not complete:
            interval = self.get_current_interval(comparison)
            if interval <= 0:
                self._alive = False
                interval = 0
        status_data = {
            'alive': self._alive,
            'current_interval': interval,
            'interval_count': self._interval_chunks,
            'complete': complete,
        }
        return status_data
