#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 13:03:35 2021

@author: maurer
"""

# https://aaronluna.dev/series/flask-api-tutorial/part-4/
from werkzeug.exceptions import Unauthorized, Forbidden
from functools import wraps
from flask import request

class SingleCredMan:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        return SingleCredMan.__instance

    @staticmethod
    def setInstance(newInst):
        SingleCredMan.__instance=newInst

def token_required(f):
    """Execute function if request contains valid access token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        _check_access_token()
        return f(*args, **kwargs)

    return decorated


def _check_access_token():
    token = request.headers.get("Authorization")
    if not token:
        raise Unauthorized(description="Unauthorized")
    man = SingleCredMan.getInstance()
    if man==None:
        raise Forbidden(description="not initialized")

    if not man.isAuthenticated(token):
        raise Forbidden(description="not authorized")
    return token


def get_header_parser(namespace):
    parser = namespace.parser()
    parser.add_argument('Authorization', location='headers', required=True)
    return parser