#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: maurer
"""

from flask_restx import fields, Model
from ocpi.models.types import role, CaseInsensitiveString
from ocpi.models.location import BusinessDetails, Image

CredentialsRole = Model('CredentialsRole', {
    'role': fields.String(enum=role, description='Type of role'),
    'business_details': fields.Nested(BusinessDetails, description='Details of this party'),
    'party_id': CaseInsensitiveString(max_length=3, description='CPO, eMSP (or other role) ID of this party (following the ISO-15118 standard).'),
    'country_code': CaseInsensitiveString(max_length=2, description='ISO-3166 alpha-2 country code of the country this party is operating in')
})

Credentials = Model('Credentials', {
    'token': fields.String(description='Case Sensitive, ASCII only.'),
    'url': fields.String(description='The URL to your API versions endpoint.'),
    'roles': fields.List(fields.Nested(CredentialsRole), description='List of the roles this party provides.')
})


def add_models_to_credentials_namespace(namespace):
    for model in [CredentialsRole, Credentials, BusinessDetails, Image]:
        namespace.models[model.name] = model