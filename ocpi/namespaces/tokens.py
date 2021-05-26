#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:03:00 2021
https://github.com/ocpi/ocpi/blob/master/mod_tokens.asciidoc
@author: gruell
"""

import logging
from flask_restx import Resource, Namespace
from flask_restx import reqparse
from flask_restx.inputs import datetime_from_iso8601
from ocpi.models import resp, respList
from ocpi.decorators import get_header_parser, token_required
from ocpi.models.location import add_models_to_location_namespace, EVSE, Location, Connector
from datetime import datetime


token_ns = Namespace(name="token", validate=True)

add_models_to_location_namespace(token_ns)
parser = get_header_parser(token_ns)

log = logging.getLogger('ocpi')


def receiver():
    #TODO: add receiver endpoints
    return token_ns


def sender():
    # TODO: add sender endpoints
    return token_ns


def makeTokenNamespace(interfaces=['SENDER', 'RECEIVER']):
    log.debug('location interfaces:'+str(interfaces))
    if 'SENDER' in interfaces:
        sender()
    if 'RECEIVER' in interfaces:
        receiver()

    return token_ns