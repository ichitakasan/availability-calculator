
from datetime import timedelta
import re
import math

DEFAULT_WEEK_DURATIONS = [24, 24, 24, 24, 24, 24, 24] # 24x7 hours
DAYS_PER_YEAR = 365.2425


# ---------------------------------------------------------------------------------------------------------------------
#     AVAILABILITY CALCULATIONS
# ---------------------------------------------------------------------------------------------------------------------

def calculate_daily_availability(td_down : timedelta) -> float:
    """
    Returns the daily availability corresponding to the down time specified in parameter.
    E.g.: down_time = 6h -> daily_SLA = 0.75 (or 75%)
    Output: between 0 and 1
    """
    seconds_count = 86400
    ret = (seconds_count - td_down.total_seconds()) / seconds_count
    return ret if ret > 0 else 0


def calculate_weekly_availability(td_down : timedelta, week_durations : list[int] = DEFAULT_WEEK_DURATIONS) -> float:
    """
    Returns the weekly availability corresponding to the down time specified in parameter.
    E.g.: down_time = 2d 6h -> weekly_SLA = 0.6785714285714286 (or 67.85714285714286%)
    Default value for the week_durations parameter is 24x7 (full time).
    Output: between 0 and 1
    """
    seconds_count = sum([(d * 3600) for d in week_durations])
    ret = (seconds_count - td_down.total_seconds()) / seconds_count
    return ret if ret > 0 else 0


def calculate_monthly_availability(td_down : timedelta, week_durations : list[int] = DEFAULT_WEEK_DURATIONS) -> float:
    """
    Returns the monthly availability corresponding to the down time specified in parameter.
    It is calculated based on an average Gregorian, solar number of days averaged over a 400-year cycle (see [https://en.wikipedia.org/wiki/Year#Summary]).
    Default value for the week_durations parameter is 24x7 (full time).
    Output: between 0 and 1
    """
    seconds_count = sum([(d * 3600) for d in week_durations]) / 7 * DAYS_PER_YEAR / 12
    ret = (seconds_count - td_down.total_seconds()) / seconds_count
    return ret if ret > 0 else 0


def calculate_quarterly_availability(td_down : timedelta, week_durations : list[int] = DEFAULT_WEEK_DURATIONS) -> float:
    """
    Returns the quarterly availability corresponding to the down time specified in parameter.
    It is calculated based on an average Gregorian, solar number of days averaged over a 400-year cycle (see [https://en.wikipedia.org/wiki/Year#Summary]).
    Default value for the week_durations parameter is 24x7 (full time).
    Output: between 0 and 1
    """
    seconds_count = sum([(d * 3600) for d in week_durations]) / 7 * DAYS_PER_YEAR / 4
    ret = (seconds_count - td_down.total_seconds()) / seconds_count
    return ret if ret > 0 else 0


def calculate_yearly_availability(td_down : timedelta, week_durations : list[int] = DEFAULT_WEEK_DURATIONS) -> float:
    """
    Returns the yearly availability corresponding to the down time specified in parameter.
    It is calculated based on an average Gregorian, solar number of days averaged over a 400-year cycle (see [https://en.wikipedia.org/wiki/Year#Summary]).
    Default value for the week_durations parameter is 24x7 (full time).
    Output: between 0 and 1
    """
    seconds_count = sum([(d * 3600) for d in week_durations]) / 7 * DAYS_PER_YEAR
    ret = (seconds_count - td_down.total_seconds()) / seconds_count
    return ret if ret > 0 else 0

# ---------------------------------------------------------------------------------------------------------------------
#     DOWNTIME CALCULATIONS
# ---------------------------------------------------------------------------------------------------------------------

def calculate_daily_downtime(f_availability : float) -> timedelta:
    """
    Returns the daily downtime corresponding to the availability specified in parameter.
    Output: timedelta
    """
    seconds_count = 86400
    ret = seconds_count * (1 - f_availability)
    return timedelta(seconds=ret)


def calculate_weekly_downtime(f_availability : float, week_durations : list[int] = DEFAULT_WEEK_DURATIONS) -> timedelta:
    """
    Returns the weekly downtime corresponding to the availability specified in parameter.
    Default value for the week_durations parameter is 24x7 (full time).
    Output: timedelta
    """
    print(f'week_durations = {week_durations}')
    seconds_count = sum([(d * 3600) for d in week_durations])
    ret = seconds_count * (1 - f_availability)
    return timedelta(seconds=ret)


def calculate_monthly_downtime(f_availability : float, week_durations : list[int] = DEFAULT_WEEK_DURATIONS) -> timedelta:
    """
    Returns the monthly downtime corresponding to the availability specified in parameter.
    Default value for the week_durations parameter is 24x7 (full time).
    Output: timedelta
    """
    seconds_count = sum([(d * 3600) for d in week_durations]) / 7 * DAYS_PER_YEAR / 12
    ret = seconds_count * (1 - f_availability)
    return timedelta(seconds=ret)


def calculate_quarterly_downtime(f_availability : float, week_durations : list[int] = DEFAULT_WEEK_DURATIONS) -> timedelta:
    """
    Returns the quarterly downtime corresponding to the availability specified in parameter.
    Default value for the week_durations parameter is 24x7 (full time).
    Output: timedelta
    """
    seconds_count = sum([(d * 3600) for d in week_durations]) / 7 * DAYS_PER_YEAR / 4
    ret = seconds_count * (1 - f_availability)
    return timedelta(seconds=ret)


def calculate_yearly_downtime(f_availability : float, week_durations : list[int] = DEFAULT_WEEK_DURATIONS) -> timedelta:
    """
    Returns the yearly downtime corresponding to the availability specified in parameter.
    Default value for the week_durations parameter is 24x7 (full time).
    Output: timedelta
    """
    seconds_count = sum([(d * 3600) for d in week_durations]) / 7 * DAYS_PER_YEAR
    ret = seconds_count * (1 - f_availability)
    return timedelta(seconds=ret)


# ---------------------------------------------------------------------------------------------------------------------
#     UTILITY FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------

def str_to_timedelta(time_str) -> timedelta:
    """
    Parse a time string e.g. (2h13m) into a timedelta object.

    Modified from virhilo's answer at https://stackoverflow.com/a/4628148/851699

    :param time_str: A string identifying a duration.  (eg. 2h13m)
    :return datetime.timedelta: A datetime.timedelta object
    """
    if time_str == None:
        return timedelta()
    
    regex = re.compile(r'^((?P<days>[\.\d]+?)d)?((?P<hours>[\.\d]+?)h)?((?P<minutes>[\.\d]+?)m)?((?P<seconds>[\.\d]+?)s)?$')
    parts = regex.match(time_str.replace(' ', ''))
    assert parts is not None, \
        f"Could not parse any time information from '{time_str}'.  Examples of valid strings: '8h', '2d 8h 5m 20s', '2m4s'"
    time_params = {name: float(param) for name, param in parts.groupdict().items() if param}
    return timedelta(**time_params)


def timedelta_to_str(t_delta) -> str:
    l_durations = []
    if t_delta.days > 0:
        l_durations.append(f'{t_delta.days}d')
    if t_delta.seconds > 0:
        sec_left : int = int((t_delta + timedelta(microseconds=500000)).seconds) # Rounding to the second
        
        hours_count : int = int(sec_left / 3600)
        if hours_count > 0:
            l_durations.append(f'{hours_count}h')
            sec_left -= hours_count * 3600
        
        minutes_count : int = int(sec_left / 60)
        if minutes_count > 0:
            l_durations.append(f'{minutes_count}m')
            sec_left -= minutes_count * 60

        if sec_left > 0:
            l_durations.append(f'{sec_left}s')
    
    return (' '.join(l_durations) if len(l_durations) > 0 else '0s')