#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 22:31:18 2021

@author: maurer
"""

from flask_restx import fields, Model

version_number = ['2.0', '2.1', '2.1.1', '2.2', '3.0']

interface_role = ['SENDER', 'RECEIVER']

module_id = ['cdrs',
             'chargingprofiles',
             'commands',
             'credentials',  # required for all
             'hubclientinfo',
             'locations',
             'sessions',
             'tariffs',
             'tokens',
             ]

Version = Model('Version', {
    'version': fields.String(enum=version_number, description='The version number.'),
    'url': fields.String(description='URL to the endpoint containing version specific information.'),
})

Endpoint = Model('Endpoint', {
    'identifier': fields.String(enum=module_id),
    'role': fields.String(enum=interface_role),
    'url': fields.String()
})


VersionsData = Model('VersionsData', {
    'versions': fields.List(fields.Nested(Version)),
})

VersionDetailsData = Model('VersionDetailsData', {
    'version': fields.String(enum=version_number, description='The version number.'),
    'endpoints': fields.List(fields.Nested(Endpoint)),
})


def add_models_to_version_namespace(namespace):
    for model in [VersionsData, VersionDetailsData, Version, Endpoint]:
        namespace.models[model.name] = model