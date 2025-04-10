from typing import Optional, Annotated
from datetime import timedelta
import os

import uvicorn
from fastapi import FastAPI, Query, Request

from exceptions import *
from functions import *


app = FastAPI()

@app.get("/")
async def status():
    return True


@app.get("/api")
async def api(request : Request,
              downtime : Annotated[str | None, Query()] = None,
              availability : Annotated[float | None, Query(min_value=0, max_value=100)] = None,
              dur : Annotated[list[int] | None, Query()] = None,
              wk : Annotated[str | None, Query(min_length=7, max_length=7)] = None):

    # Error handling
    if not downtime and not availability:
        raise ParameterException(f'Parameter "downtime" or "availability" misssing')
    if downtime and availability:
        raise ParameterException(f'Parameter "downtime" or "availability" cannot be used in the same query')
    if dur and wk:
        raise ParameterException(f'Parameters "dur" and "wk" cannot be used in the same query')
    if dur:
        for d in dur:
            if d < 0 or d > 24:
                raise ParameterException(f'Parameter "dur={d}" out of range [0, 24]')
    if wk:
        for d in wk:
            if d < 'a' or d > 'y':
                raise ParameterException(f'Letters in "wk={wk}" should be between \'a\' (0) and \'y\' (24)')
    
    # Query parameters processing
    week_durations = None # Can be passed as null to the calculation functions
    if dur:
        week_durations = [d for d in dur]
    elif wk:
        week_durations = [ord(d) - ord('a') for d in wk]
    
    # Calculation
    request_url = f'{request.base_url}{request.url.path[1:]}'
    if downtime:
        return calculate_availability(downtime, week_durations, request_url)
    elif availability:
        return calculate_downtime(availability, week_durations, request_url)
    else:
        raise ParameterException(f'API Error: no downtime nor availability found')


def calculate_availability(downtime, week_durations, request_url) -> dict:
    """
    Returns the availability (in %) based on the downtime in parameter.
    """
    td_down : timedelta = str_to_timedelta(downtime)

    downtimeSecs = int(td_down.total_seconds())
    downtime = timedelta_to_str(td_down)

    if week_durations:
        avail_week = calculate_weekly_availability(td_down, week_durations)
        avail_month = calculate_monthly_availability(td_down, week_durations)
        avail_quarter = calculate_quarterly_availability(td_down, week_durations)
        avail_year = calculate_yearly_availability(td_down, week_durations)
        wk = ''.join([chr(ord('a') + d) for d in week_durations])
        return {
            'downtimeSecs' : downtimeSecs,
            'downtime' : downtime,
            'weekDurations' : week_durations,
            'downtimeURL' : f'{request_url}?downtime={downtime}&wk={wk}',
            'availability' : {
                'week': avail_week * 100,
                'month': avail_month * 100,
                'quarter': avail_quarter * 100,
                'year': avail_year * 100,
            }
        }
    else:
        avail_day = calculate_daily_availability(td_down)
        avail_week = calculate_weekly_availability(td_down)
        avail_month = calculate_monthly_availability(td_down)
        avail_quarter = calculate_quarterly_availability(td_down)
        avail_year = calculate_yearly_availability(td_down)
        return {
            'downtimeSecs' : downtimeSecs,
            'downtime' : downtime,
            'URL' : f'{request_url}?downtime={downtime}',
            'availability' : {
                'day': avail_day * 100,
                'week': avail_week * 100,
                'month': avail_month * 100,
                'quarter': avail_quarter * 100,
                'year': avail_year * 100,
            }
        }


def calculate_downtime(availability, week_durations, request_url) -> dict:
    """
    Returns the downtime (in sec) based on the availability in parameter.
    """
    f_availability : float = availability / 100

    if week_durations:
        downtime_week = calculate_weekly_downtime(f_availability, week_durations)
        downtime_month = calculate_monthly_downtime(f_availability, week_durations)
        downtime_quarter = calculate_quarterly_downtime(f_availability, week_durations)
        downtime_year = calculate_yearly_downtime(f_availability, week_durations)
        wk = ''.join([chr(ord('a') + d) for d in week_durations])
        return {
            'availability' : availability,
            'weekDurations' : week_durations,
            'url' : f'{request_url}?availability={availability}&wk={wk}',
            'downtime' : {
                'week': timedelta_to_str(downtime_week),
                'month': timedelta_to_str(downtime_month),
                'quarter': timedelta_to_str(downtime_quarter),
                'year': timedelta_to_str(downtime_year),
            }
        }
    else:
        downtime_day = calculate_daily_downtime(f_availability)
        downtime_week = calculate_weekly_downtime(f_availability)
        downtime_month = calculate_monthly_downtime(f_availability)
        downtime_quarter = calculate_quarterly_downtime(f_availability)
        downtime_year = calculate_yearly_downtime(f_availability)
        return {
            'availability' : availability,
            'url' : f'{request_url}?availability={availability}',
            'downtime' : {
                'daySecs' : downtime_day.total_seconds(),
                'day': timedelta_to_str(downtime_day),
                'weekSecs' : downtime_week.total_seconds(),
                'week': timedelta_to_str(downtime_week),
                'monthSecs' : downtime_month.total_seconds(),
                'month': timedelta_to_str(downtime_month),
                'quarterSecs' : downtime_quarter.total_seconds(),
                'quarter': timedelta_to_str(downtime_quarter),
                'yearSecs' : downtime_year.total_seconds(),
                'year': timedelta_to_str(downtime_year),
            }
        }

if __name__ == "__main__":
    PORT = 8000
    uvicorn.run(app, port=PORT)