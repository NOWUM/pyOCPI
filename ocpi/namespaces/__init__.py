#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://aaronluna.dev/series/flask-api-tutorial/part-4/
import base64
from werkzeug.exceptions import Unauthorized, Forbidden
from functools import wraps
from flask import request
from flask_restx import reqparse
from flask_restx.inputs import datetime_from_iso8601
from datetime import datetime
import ocpi.exceptions as oe

import logging

log = logging.getLogger('ocpi')


class SingleCredMan:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        return SingleCredMan.__instance

    @staticmethod
    def setInstance(newInst):
        SingleCredMan.__instance = newInst


def token_required(f):
    """Execute function if request contains valid access token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        _check_access_token()
        return f(*args, **kwargs)

    return decorated


def pagination_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('from', type=datetime_from_iso8601,
                        default='2021-01-01T13:30:00+02:00')
    parser.add_argument('to', type=datetime_from_iso8601,
                        default='2038-01-01T13:30:00+02:00')
    parser.add_argument('offset', type=int, default=0)
    parser.add_argument('limit', type=int, default=50)
    return parser

def _check_access_token():
    authToken = request.headers.get("Authorization")
    if not authToken:
        raise Unauthorized(description="Unauthorized")

    token = authToken.replace('Token ', '').strip()
    man = SingleCredMan.getInstance()
    if man == None:
        raise Forbidden(description="not initialized")

    try:
        decodedToken = base64.b64decode(token).decode('utf-8')
        if not (man.isAuthenticated(decodedToken)):
            raise Forbidden(description="not authorized")
        return decodedToken
    except Exception:
        # accept plain token as token if not base64
        log.warning('token was not sent as base64 - trying plain')
        if not man.isAuthenticated(token):
            raise Forbidden(description="not authorized")
    return token


def get_header_parser(namespace):
    parser = namespace.parser()
    parser.add_argument('Authorization', location='headers', required=True)
    parser.add_argument('X-Request-ID', required=True, location='headers')
    parser.add_argument('X-Correlation-ID', location='headers')

    return parser

def make_response(function, *args, **kwargs):
    headers=None
    http_code=200
    status_message = 'OK'
    status_code = 1000
    data = []
    try:
        result = function(*args, **kwargs)
        if type(result) == tuple:
            data, headers = result
        else:
            data = result
    except oe.OcpiError as e:
        status_message = e.message
        status_code = e.status_code
    except Exception as e:
        status_message = f'Error {e}'
        status_code = 3000

    return {'data': data,
            'status_code': status_code,
            'status_message': status_message,
            'timestamp': datetime.now()
            }, http_code, headers


if __name__ == '__main__':
    def raisUnsupVers(input_):
        print(input_)
        raise oe.UnsupportedVersionError('should be 2.2')
    print(make_response(raisUnsupVers, 4))

    def testTuple(input_):
        return input_, {'Authorization': 'TEST'}
    print(make_response(testTuple, 4))