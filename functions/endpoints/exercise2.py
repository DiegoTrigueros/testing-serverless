from utils import Response
from database.database import Connection
from bson.objectid import ObjectId
from functions.endpoints.DataPreparation import prepare_data

conn = Connection.get_instance()


def get_weekday_name(week_number: int) -> str:
    days = {
        1: "monday",
        2: "tuesday",
        3: "wednesday",
        4: "thursday",
        5: "friday",
        6: "saturday",
        7: "sunday"
    }

    return days[week_number]


def get_formatted_date(hour: str) -> str:
    return f"{hour}:00 - {hour}:59"


def second_function(headers) -> dict:
    if ("enterprise" in headers) and ("store" in headers) \
            and ("timezone" in headers) and ("date_range" in headers):
        enterprise, store, date_to, date_from = prepare_data(
            headers)
        pipeline = [
            {
                '$match': {
                    'datetime': {
                        '$gt': date_from,
                        '$lte': date_to
                    },
                    'store': ObjectId(store),
                    'enterprise': ObjectId(enterprise)
                }
            }, {
                '$group': {
                    '_id': {
                        'weekday': {
                            '$isoDayOfWeek': '$datetime'
                        },
                        'gender': '$gender',
                        'hour': {
                            '$hour': '$datetime'
                        }
                    },
                    'visitors': {
                        '$sum': 1
                    }
                }
            }, {
                '$sort': {
                    '_id': 1
                }
            }
        ]

        data = conn.entrances.aggregate(pipeline)
        result = dict()

        if data is not None:
            for d in data:
                day_of_week = d['_id']['weekday']
                hour = str(d['_id']['hour']).zfill(2)
                gender = d['_id']['gender']
                visitors = d['visitors']
                weekday_name = get_weekday_name(day_of_week)
                if weekday_name not in result:
                    result[weekday_name] = {
                        "total": {
                            "male": 0,
                            "female": 0
                        },
                        "hourly": {get_formatted_date(str(i).zfill(2)): {
                                    "male": 0,
                                    "female": 0
                                    } for i in range(0, 24)}
                    }
                result[weekday_name]["total"][gender] += visitors
                result[weekday_name]["hourly"][f"{hour}:00 - {hour}:59"][
                    gender] += \
                    visitors
            return Response.success_message(200, result).result
        return Response.fail_message(404, {"message": "no data found"}).result

