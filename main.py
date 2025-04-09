from typing import Optional, Annotated
from datetime import timedelta
import os

import uvicorn
from fastapi import FastAPI, Query
from dotenv import load_dotenv

from exceptions import *
from functions import *


load_dotenv()
REQUIRED_ENVIRONMENT_VARIABLES = ['HOST', 'PORT']
for e in REQUIRED_ENVIRONMENT_VARIABLES:
    if e not in os.environ:
        raise EnvironmentError(f'Undefined environment variable {e}')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

app = FastAPI()

@app.get("/")
async def status():
    return True


@app.get("/api")
async def api(downtime: Annotated[str | None, Query()] = None,
              dur: Annotated[list[int] | None, Query()] = None,
              wk: Annotated[str | None, Query(min_length=7, max_length=7)] = None):

    print(f'downtime = {downtime}')
    print(f'dur = {dur}')
    print(f'wk = {wk}')
    # Error handling
    if not downtime:
        raise ParameterException(f'Parameter "downtime" misssing')
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
    week_durations = None
    if not dur and not wk: # No weekly timings specified
        week_durations = [24] * 7
    elif dur:
        week_durations = [d for d in dur]
    elif wk:
        week_durations = [ord(d) - ord('a') for d in wk]
    
    return calculate_availability(downtime, week_durations)

def calculate_availability(downtime, week_durations) -> dict:
    """
    Returns the availability based on the downtime in parameter.
    """
    td_down : timedelta = str_to_timedelta(downtime)

    downtimeSecs = int(td_down.total_seconds())
    downtime = timedelta_to_str(td_down)
    weeklySLA = calculate_weeklySLA(td_down, week_durations)
    monthlySLA = calculate_monthlySLA(td_down, week_durations)
    quarterlySLA = calculate_quarterlySLA(td_down, week_durations)
    yearlySLA = calculate_yearlySLA(td_down, week_durations)

    if week_durations:
        wk = ''.join([chr(ord('a') + d) for d in week_durations])
        return {
            'downtimeSecs' : downtimeSecs,
            'downtime' : downtime,
            'weekDurations' : week_durations,
            'downtimeURL' : f'https://{HOST}:{PORT}{app.url_path_for('api')}?downtime={downtime}&wk={wk}',
            'weeklySLA': weeklySLA * 100,
            'monthlySLA': monthlySLA * 100,
            'quarterlySLA': quarterlySLA * 100,
            'yearlySLA': yearlySLA * 100,
        }
    else:
        dailySLA = calculate_dailySLA(td_down)
        return {
            'downtimeSecs' : downtimeSecs,
            'downtime' : downtime,
            'downtimeURL' : f'https://{HOST}:{PORT}{app.url_path_for('api')}?downtime={downtime}',
            'dailySLA': dailySLA * 100,
            'weeklySLA': weeklySLA * 100,
            'monthlySLA': monthlySLA * 100,
            'quarterlySLA': quarterlySLA * 100,
            'yearlySLA': yearlySLA * 100,
        }


if __name__ == "__main__":
    uvicorn.run(app, port=int(PORT))