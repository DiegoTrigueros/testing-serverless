try:
    import unzip_requirements
except ImportError:
    pass

from functions import endpoints


def handler(event, context) -> object:
    resource = event['resource']
    headers = event['headers']
    body = event['body']

    if resource == '/exercise1':
        return endpoints.exercise1.first_function(headers)
    elif resource == '/exercise2':
        return endpoints.exercise2.second_function(headers)
    elif resource == '/exercise3':
        return endpoints.exercise3.third_function(headers)