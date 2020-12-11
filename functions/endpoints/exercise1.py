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
        if data is not None:
            response = {
                "female": 0,
                "male": 0,
                "total_visits": 0,
                "highest_temperature": 0
            }

            temperatures_set = set()
            for d in data:
                response[d['_id']] += d['total_visits']
                response['total_visits'] += d['total_visits']

                temperatures_set.add(d['highest_temperature'])

            response['highest_temperature'] = max(temperatures_set)

            return Response.success_message(200, response).result
        else:
            response = {
                "error": 404
            }
            return Response.success_message(200, response).result
    else:
        return Response.fail_message(404, {"message": "headers do not "
                                                      "contain needed data"})



