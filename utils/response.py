import json
import bson
from typing import Optional


class Response:
    SUCCESS = 'success'
    FAIL = 'fail'
    ERROR = 'error'

    def __init__(self, result):
        self.result = result

    @property
    def result(self) -> dict:
        return self.__result

    @result.setter
    def result(self, data_result: dict):
        if not isinstance(data_result, dict):
            raise TypeError("data_result argument must be a dict")
        self.__result = data_result

    @classmethod
    def success_message(cls, code: int, data: dict):
        # Validations
        if not isinstance(code, int):
            raise TypeError('code argument must be an integer')
        if not isinstance(data, dict):
            raise TypeError('data argument must be a dict')

        # Definition
        response = {
            'status': cls.SUCCESS,
            'data': data
        }
        output = cls.parse_to_output_format(code, response)
        return cls(output)

    @classmethod
    def fail_message(cls, code: int, data: dict):
        # Validations
        if not isinstance(code, int):
            raise TypeError('code argument must be an integer')
        if not isinstance(data, dict):
            raise TypeError('data argument must be a dict')

        # Definition
        response = {
            'status': cls.FAIL,
            'data': data
        }
        output = cls.parse_to_output_format(code, response)
        return cls(output)

    @classmethod
    def error_message(cls, code: int,
                      message: str, data: Optional[dict] = None):
        # Validations
        if not isinstance(code, int):
            raise TypeError('code argument must be an integer')
        if not isinstance(message, str):
            raise TypeError('message argument must be a string')
        if data is not None and not isinstance(data, dict):
            raise TypeError('data argument must be a dict')

        # Definition
        response = {
            'status': cls.ERROR,
            'message': message
        }
        if data is not None:
            response.update({'data': data})
        output = cls.parse_to_output_format(code, response)
        return cls(output)

    @staticmethod
    def parse_to_output_format(code: int, response: dict):
        return {
            'statusCode': code,
            'body': json.dumps(response, default=Response.custom_encoder)
        }

    @staticmethod
    def custom_encoder(x):
        if isinstance(x, bson.objectid.ObjectId):
            return str(x)
        else:
            raise TypeError('x argument is not valid in encoder_custom')