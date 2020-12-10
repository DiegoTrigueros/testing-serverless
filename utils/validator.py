import json
from bson import ObjectId
from typing import List, Union, Dict


class Validator:
    @staticmethod
    def validate_headers(headers: dict, mandatory: list) -> List[Union[bool, Dict[str, list]]]:
        if not isinstance(headers, dict):
            raise TypeError('headers argument must be a dict')
        if not isinstance(mandatory, list):
            raise TypeError('mandatory argument must be a list')

        missed = [arg[0] for arg in mandatory if arg[0] not in headers.keys()]
        response = {
            'headers_required': missed
        }

        if not missed:
            return [False, None]
        return [True, response]

    @staticmethod
    def get_mandatory_headers(headers, mandatory):
        new = dict()
        for header in mandatory:
            header_name, header_type = header[:2]
            if header_type is not str:
                new[header_name] = json.loads(headers[header_name])
            else:
                new[header_name] = headers[header_name]

        return new

    @staticmethod
    def validate_type_headers(headers, mandatory):
        if not isinstance(headers, dict):
            raise TypeError('headers argument must be a dict')
        if not isinstance(mandatory, list):
            raise TypeError('mandatory_headers argument must be a list')

        w = list()
        for m in mandatory:
            # Each element is (name, type) or (name, type, subtype)
            header_name, header_type = m[:2]

            # Get element
            element = headers[header_name]

            # Check if variable "m" has subtype (it's in the index 2)
            if len(m) == 3:
                header_subtype = m[2]

                # Validations for elements with subtypes
                if header_type is list:
                    if not all(isinstance(x, header_subtype) for x in element):
                        w.append(f'{header_name} is not a list of {header_subtype}')

            # Validations for elements without subtypes
            if not isinstance(element, header_type):
                w.append(f'{header_name} is not a(n) {header_type.__name__}')
            if 'id' in header_name and not ObjectId.is_valid(element):
                w.append(f'{header_name} is not a valid ObjectId')

        if not w:
            return [False, None]
        wrong = {'wrong_type': w}
        return [True, wrong]

    @classmethod
    def headers_complete_validation(cls, headers, mandatory_headers):
        # Validate mandatory headers
        miss, data = cls.validate_headers(headers, mandatory_headers)
        if miss:
            return [miss, data]

        # Get headers
        headers = cls.get_mandatory_headers(headers, mandatory_headers)

        # Validate types in headers
        wrong, data = cls.validate_type_headers(
            headers, mandatory_headers
        )
        if wrong:
            return [wrong, data]

        return [False, headers]

    @classmethod
    def validate_keys(cls, data: dict, valid_keys):
        wrong_keys = [k for k in data if k not in valid_keys]
        if not wrong_keys:
            return [False, None]
        return [True, wrong_keys]