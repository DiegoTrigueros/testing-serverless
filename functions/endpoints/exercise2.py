from utils import Response
from database.database import Connection
from bson.objectid import ObjectId
from functions.endpoints.DataPreparation import prepare_data

conn = Connection.get_instance()


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
            }
        ]

        data = conn.entrances.aggregate(pipeline)

        for d in data:
            index = d['_id']
            weekday = index['weekday']
            gender = index['gender']
            hour = index['hour']

        response = {
            "message": "successful"
        }
    else:
        response = {
            "message": "404"
        }

    return Response.success_message(200, response).result

