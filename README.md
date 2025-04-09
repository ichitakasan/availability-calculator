# Availability Calculator

Calculates daily, weekly, monthly, and yearly availability based on a down time and vice versa.

# Usage (API)

/api?downtime=<duration>[&wk=<week_durations>]

With:
* downtime=<duration> in the form "XXdXXhXXmXXs" (e.g. "3d6h" or "1h 12m 25s")
* wk=<week_duration> in the form "[a-y]{7}", with a=0, b=2, ..., y=24 (e.g. "iiiiaa" for "8 hours 5 days a week and 0 hours during weekend")
Note: the order of days (e.g. first day being Sunday or Monday) does not have any impact on the final calculation.

Example:
/api?downtime=9h8m6s&wk=iiiiiaa
/api?downtime=10m5s
/api?downtime=6h10m&dur=5&dur=5&dur=5&dur=5&dur=5&dur=0&dur=0

# Run

With the Python virtualenv activated:
`fastapi dev main.py`

Other ways:
* In development
`uvicorn main:app --port 3000`
* In production
`gunicorn -k uvicorn.workers.UvicornWorker -w 4 --bind 0.0.0.0:5000 main:app`

On Windows:
`python main.py`
