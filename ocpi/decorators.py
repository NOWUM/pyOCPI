#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 13:03:35 2021

@author: maurer
"""

# https://aaronluna.dev/series/flask-api-tutorial/part-4/
import secrets
import base64
from werkzeug.exceptions import Unauthorized, Forbidden
from functools import wraps
from flask import request
from flask_restx import reqparse
from flask_restx.inputs import datetime_from_iso8601
from datetime import datetime

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


def createOcpiHeader(token):
    encToken = base64.b64encode(token.encode("utf-8")).decode('utf-8')
    return {
        'Authorization': 'Token '+encToken,
        'X-Request-ID': secrets.token_urlsafe(8)
    }


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
    except:
        # accept plain token as token if not base64
        log.error('token was not sent as base64')
        if not man.isAuthenticated(token):
            raise Forbidden(description="not authorized")
    return token


def get_header_parser(namespace):
    parser = namespace.parser()
    parser.add_argument('Authorization', location='headers', required=True)
    parser.add_argument('X-Request-ID', required=True, location='headers')
    parser.add_argument('X-Correlation-ID', location='headers')

    return parser


def makeResponse(data, status_code=1000, message='nothing',
                 timestamp=None, http_code=200,
                 headers=None):
    return {'data': data,
            'status_code': status_code,
            'status_message': message,
            'timestamp': timestamp or datetime.now(),
            }, http_code, headers