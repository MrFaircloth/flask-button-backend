from datetime import datetime
from copy import deepcopy

from util import parse_time_string, get_future_timestamp, get_time_difference


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
        interval_time_total: str = "3d",
        interval_chunks_count: int = 10,
    ) -> None:
        self._init_date = datetime.now()

        self._total_time = parse_time_string(total_time)
        interval_time = parse_time_string(interval_time_total)
        self._interval_time = interval_time / interval_chunks_count
        self.interval_chunks_count = interval_chunks_count

        self._alive = True
        self._complete_date = get_future_timestamp(self._total_time)
        self._interval_chunks = []
        self.reset()

    def _set_interval_chunks(self):
        '''
        Creates a list of datetimes in descending order.
        These timestamps will be used as markers to determine where the button current interval is.
        '''
        chunks = []
        current = datetime.now()
        for _ in range(self.interval_chunks_count):
            current = get_future_timestamp(
                self._interval_time, current
            )
            chunks.append(current)
        # make sure the older timestamps are at the start
        chunks.sort(reverse=True)
        self._interval_chunks = chunks

    def _is_complete(self) -> bool:
        '''
        If past the determined end time and still living, returns True
        '''
        now = datetime.now()
        return now > self._complete_date and self._alive

    def reset(self) -> None:
        '''
        Resets the button intervals.
        Setting the current interval to the maximum and setting the future timestamp to the interval hour setting.
        '''
        self._set_interval_chunks()

    def get_current_interval(self) -> int:
        '''
        Get's the current interval and advances if time is past due.
        '''
        now = datetime.now()
        chunks = deepcopy(self._interval_chunks)
        # remove any old timestamps
        chunks = [dt for dt in chunks if dt >= now]
        chunks.sort(reverse=True)
        # Logic behind this:
        # If there are no more chunks, it means the button can no longer be saved.
        # If the last (first due to desc ordering) datetime interval within chunks is greater than the completion datetime,
        # it means button has survived.
        if len(chunks) == 0 and len(self._interval_chunks):
            if self._complete_date > self._interval_chunks[0]:
                self._alive = False
        self._interval_chunks = chunks

        return len(self._interval_chunks)

    def _build_status(self):
        status_data = {
            'current_interval': self.get_current_interval(),
            'complete': self._is_complete(),
            'alive': self._alive,
            'interval_count': self.interval_chunks_count,
            'time_alive': get_time_difference(self._init_date, datetime.now()),
        }
        return status_data

    def get_status(self) -> dict:
        '''
        Obtains and returns button status.
        '''
        return self._build_status()
    

    def debug(self) -> dict:
        keys = ['_total_time', '_interval_time', 'interval_chunks_count', 'interval_chunks_count', '_alive', '_complete_date', '_interval_chunks']
        
        state = { key: str(self.__dict__[key]) for key in keys }
        now = datetime.now()
        
        time_left =  (self._interval_chunks[0] - now).seconds if self._interval_chunks[0] else None
        state['time_left'] = time_left
        return state
