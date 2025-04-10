# Availability Calculator

Calculates daily, weekly, monthly, and yearly availability based on a down time and vice versa.

# Usage (API)

## Availability Calculation

```
/api?downtime=<duration>[&wk=<week_durations>]
```

With:
* `downtime=<duration>` in the form `"XXdXXhXXmXXs"` (e.g. `"3d6h"` or `"1h 12m 25s"`)
* `wk=<week_duration>` in the form `"[a-y]{7}"`, with `a=0, b=2, ..., y=24` (e.g. `"iiiiaa"` for `"8 hours 5 days a week and 0 hours during weekend"`)
Note: the order of days (e.g. first day being Sunday or Monday) does not have any impact on the final calculation.

Examples:
```
/api?downtime=9h8m6s&wk=iiiiiaa
/api?downtime=10m5s
/api?downtime=6h10m&dur=5&dur=5&dur=5&dur=5&dur=5&dur=0&dur=0
```

## Downtime Calculation

```
/api?availability=<percentage>[&wk=<week_durations>]
```

With:
* `availability=<percentage>` between `0` and `100`
* `wk=<week_duration>` in the form `"[a-y]{7}"`, with `a=0, b=2, ..., y=24` (e.g. `"iiiiaa"` for `"8 hours 5 days a week and 0 hours during weekend"`)
Note: the order of days (e.g. first day being Sunday or Monday) does not have any impact on the final calculation.

Examples:
```
/api?availability=99.9&wk=iiiiiaa
/api?availability=80.0
/api?availability=99.999&dur=5&dur=5&dur=5&dur=5&dur=5&dur=0&dur=0
```

# Run

## Development

With the Python virtualenv activated:
```bash
fastapi dev app/main.py   # Uses default port 8000
fastapi dev app/main.py --port 9999
```

## Production

```bash
fastapi run app/main.py   # Uses default port 8000
fastapi run app/main.py --port 80

# If running behind a proxy like Nginx or Traefik add --proxy-headers
fastapi run app/main.py --port 80 --proxy-headers
```

## Other Ways

```bash
# In development (cd into app/ directory first)
uvicorn main:app --port 3000 [--reload] # Optional automatic reload
# In development (using coded uvicorn in "__main__" function)
python app/main.py

# In production (NOT WORKING ON WINDOWS!)
gunicorn -k uvicorn.workers.UvicornWorker -w 4 --bind 0.0.0.0:5000 main:app
```
