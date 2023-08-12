from datetime import datetime, timedelta
from copy import deepcopy
from typing import List
import logging


from .util import (
    parse_time_string,
    get_future_timestamp,
    get_time_difference,
    create_deltas,
    create_intervals,
)


class Button:
    '''
    Purpose: The Button was designed to function similar to a timer.
    The goal of the button is to remain 'alive' until it reaches its completion date.
    The timer length is determined by the provided interval and it will be broken up into chunks.
    These chunks give a rough estimate of how far along the button is.
    Once it reaches 0, the button's 'alive' status will be set to false and will become inoperable.
    The status of the button will only be known once checked.
    Upon checking, it report its alive status and it's current interval chunk along with any other relevant data.
    '''

    def __init__(
        self,
        total_time: str = "14d",
        total_life_time: str = "3d",
        deviation_time: str = '30m',
        interval_chunks_count: int = 10,
    ) -> None:
        self._creation_date = datetime.now()

        self._total_game_time = parse_time_string(total_time)
        self._total_life_time = parse_time_string(total_life_time)
        self._deviation_time = parse_time_string(deviation_time)
        self.interval_chunks_count = interval_chunks_count
        self._interval_time_deltas = create_deltas(
            self._total_life_time, self._deviation_time, self.interval_chunks_count
        )
        self._alive = True
        self._completion_date = get_future_timestamp(self._total_game_time)

        self._interval_times = []
        self.reset()

    def _state_override(self, state_values: dict) -> None:
        '''
        In the event of an error, the button's active state can be set here.
        See accompanying model in models.py for state values.
        '''
        logging.info('Overriding button configurations with state values.')
        value_pairings = {
            '_creation_date': 'creation_date',
            '_completion_date': 'completion_date',
            '_interval_time_deltas': 'delta_times',
            '_interval_times': 'interval_times',
        }
        for key in value_pairings:
            self.__dict__[key] = state_values.get(
                value_pairings[key], self.__dict__[key]
            )
        self.__dict__
        self._creation_date = state_values['creation_date']
        self._completion_date = state_values['completion_date']
        self._interval_time_deltas = [
            timedelta(seconds=td) for td in state_values['delta_times']
        ]
        self._interval_times = [
            datetime.fromisoformat(dt) for dt in state_values['interval_times']
        ]

    def _is_complete(self) -> bool:
        '''
        If past the determined end time and still living, returns True
        '''
        now = datetime.now()
        return now > self._completion_date and self._alive

    def reset(self) -> None:
        '''
        Resets the button intervals.
        Setting the current interval to the maximum and setting the future timestamp to the interval hour setting.
        '''
        logging.info('Button state reset.')
        self._interval_times = create_intervals(
            datetime.now(), self._interval_time_deltas
        )

    @classmethod
    def _remove_expired_intervals(
        cls, intervals: List[datetime], cutoff: datetime = None
    ) -> List[datetime]:
        '''
        Logic handler to remove datetimes which are older than the given cutoffpoint.
        Default cutoff = datetime.now()
        '''
        logging.debug('Removing expired interval values.')
        cutoff = datetime.now() if not cutoff else cutoff
        intervals = [dt for dt in intervals if dt >= cutoff]
        intervals.sort(reverse=True)
        return intervals

    def get_current_interval(self) -> int:
        '''
        Get's the current interval. Updates button alive / completion status if necessary.
        '''
        now = datetime.now()
        intervals = deepcopy(self._interval_times)
        intervals = self._remove_expired_intervals(intervals, now)

        # Logic behind this:
        # If there are no more chunks, it means the button can no longer be saved.
        # If the last (first due to desc ordering) datetime interval within chunks is greater than the completion datetime,
        # it means button has survived.
        if len(intervals) == 0 and len(self._interval_times):
            if self._completion_date > self._interval_times[0]:
                self._alive = False
                print('The button is no longer alive...')
        self._interval_times = intervals
        logging.debug(f"Current button interval: {len(self._interval_times)}")
        return len(self._interval_times)

    def _build_status(self) -> dict:
        '''
        Builds out a dictionary describing the current button status.
        Designed to be mildly vague and only providing the necessary information to play the game.
        '''
        status_data = {
            'current_interval': self.get_current_interval(),
            'complete': self._is_complete(),
            'alive': self._alive,
            'interval_count': self.interval_chunks_count,
            'time_alive': get_time_difference(self._creation_date, datetime.now()),
        }
        return status_data

    def get_status(self) -> dict:
        '''
        Obtains and returns button status.
        '''
        return self._build_status()

    def debug(self) -> dict:
        state = {}

        state['total_game_time_hours'] = self._total_game_time.total_seconds() / 60 / 60
        state['interval_chunks_count'] = self.interval_chunks_count
        state['alive'] = self._alive
        state['complete'] = self._is_complete()
        state['completion_date'] = self._completion_date.isoformat()
        state['interval_time_deltas_seconds'] = [
            delta.total_seconds() for delta in self._interval_time_deltas
        ]
        state['interval_times_epoch_seconds'] = [dt.isoformat() for dt in self._interval_times]

        now = datetime.now()
        time_left = 'None'
        if self._interval_times:
            time_left = (
                int((self._interval_times[0] - now).total_seconds())
                if self._interval_times[0]
                else None
            )
        state['time_left'] = time_left
        return state
