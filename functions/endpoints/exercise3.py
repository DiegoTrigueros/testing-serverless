from utils import Response
from database.database import Connection
from bson.objectid import ObjectId

conn = Connection.get_instance()


def third_function(headers):
    if ('coordinates' in headers) and ('enterprise' in headers):
        coords = headers['coordinates']
        enterprise = headers['enterprise']
        print(coords)
        coords = coords[1:-1]
        coords = coords.split(',')

        x_coord, y_coord = coords
        x_coord = float(x_coord)
        y_coord = float(y_coord)
        pipeline = [
            {
                '$geoNear': {
                    'near': {
                        'type': 'point',
                        'coordinates': [
                            x_coord, y_coord
                        ]
                    },
                    'distanceField': 'distance',
                    'query': {
                        'enterprise': ObjectId(enterprise)
                    },
                    'spherical': True,
                    'distanceMultiplier': 0.001
                }
            }
        ]

        data = conn.stores.aggregate(pipeline)
        nearest = {}

        for d in data:
            nearest = d
            break

        message = {
            "nearest_store_id": nearest['_id'],
            "nearest_store_name": nearest['name'],
            "distance": nearest['distance']
        }
    else:
        message = {
            "error": 404
        }

    return Response.success_message(200, message).result
