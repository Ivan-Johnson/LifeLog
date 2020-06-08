import time
import urllib
from http import HTTPStatus

import LifeLogServer

AUTH_HEADER='token'
AUTH_TOKEN='test-key'
AUTH_USERID='cf1f8a6d-c3de-4987-9478-ed14fff7fe33'
AUTH_TOKEN_BAD=AUTH_TOKEN+'oiawejklfxcvkjlweeeoisdvwe'

AUTH_HEADERS={AUTH_HEADER: AUTH_TOKEN}

AUTH_USERID_1='32e6f3bd-f9ca-48db-8ee4-dc1fd1dc4f38'
AUTH_TOKEN_1='test-key-1'

def run_tests(method, url, given_headers={}, expected_status=HTTPStatus.OK):
    assert expected_status != HTTPStatus.UNAUTHORIZED
    assert expected_status != HTTPStatus.FORBIDDEN
    assert AUTH_HEADER not in given_headers

    response = method(url, headers=given_headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    headers = given_headers.copy()
    headers[AUTH_HEADER]= AUTH_TOKEN_BAD
    response = method(url, headers=headers)
    assert response.status_code == HTTPStatus.FORBIDDEN

    headers = given_headers.copy()
    headers[AUTH_HEADER]= AUTH_TOKEN
    response = method(url, headers=headers)
    assert response.status_code == expected_status
