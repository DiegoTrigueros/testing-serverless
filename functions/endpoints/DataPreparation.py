import pytz
from dateutil.parser import parse


def prepare_data(headers):
    enterprise = headers["enterprise"]
    store = headers['store']

    local_timezone_name = headers["timezone"]
    local_timezone = pytz.timezone(local_timezone_name)

    date_range = headers["date_range"]
    date_range = date_range[1:-1]
    date_range = date_range.split(',')

    date_from = date_range[0]
    date_from = date_from[1:-1]
    date_from_obj = parse(date_from)
    local_date_from = local_timezone.localize(date_from_obj)
    utc_date_from = local_date_from.astimezone(pytz.utc)

    date_to = date_range[1]
    date_to = date_to[2:-1]
    date_to_obj = parse(date_to)
    local_date_to = local_timezone.localize(date_to_obj)
    utc_date_to = local_date_to.astimezone(pytz.utc)
    return_array = [enterprise, store, utc_date_to, utc_date_from]

    return return_array
