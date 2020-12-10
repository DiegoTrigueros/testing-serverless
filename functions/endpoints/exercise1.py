from utils import Response
from database.database import Connection
from bson.objectid import ObjectId
from functions.endpoints.DataPreparation import prepare_data
conn = Connection.get_instance()


def first_function(headers) -> dict:
    if ("enterprise" in headers) and ("store" in headers) \
            and ("timezone" in headers) and ("date_range" in headers):
        enterprise, store, utc_date_to, utc_date_from = prepare_data(headers)

        pipeline = [
            {
                '$match': {
                    'enterprise': ObjectId(enterprise),
                    'store': ObjectId(store),
                    'datetime': {
                        '$gt': utc_date_from,
                        '$lte': utc_date_to
                    }
                }
            },
            {
                '$group':
                    {
                        '_id': '$gender',
                        'total_visits': {
                            '$sum': 1
                        },
                        'highest_temperature': {
                            '$max': '$temperature'
                        }
                    }
            }
        ]

        data = conn.entrances.aggregate(pipeline)

        male_visits = 0
        female_visits = 0
        max_temperature = 0
        for d in data:
            if d['_id'] == 'male':
                male_visits = d['total_visits']
            else:
                female_visits = d['total_visits']

            if d['highest_temperature'] > max_temperature:
                max_temperature = d['highest_temperature']

        total_visits = female_visits + male_visits
        response = {
            "female_visits": female_visits,
            "male_visits": male_visits,
            "total_visits": total_visits,
            "highest_temperature": max_temperature
        }
    else:
        response = {
            "error": 404
        }

    return Response.success_message(200, response).result
