#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 18:02:46 2021

@author: maurer

Api definition file
"""

from flask import Blueprint
from flask_restx import Api

from ocpi.namespaces.commands import commands_ns
from ocpi.namespaces.sessions import makeSessionNamespace
from ocpi.namespaces.locations import makeLocationNamespace
from ocpi.namespaces.versions import versions_ns
from ocpi.namespaces.reservation import reservation_ns
from ocpi.namespaces.credentials import credentials_ns
from ocpi.decorators import SingleCredMan
from ocpi.managers import VersionManager
import logging

log = logging.getLogger('ocpi')

injected = {
    'credentials': None,
    'locations': None,
    'versions': None,
    'commands': None,
    'sessions': None,
    'reservations': None,
}


def createOcpiBlueprint(base_url, injected_objects=injected, roles=['SENDER', 'RECEIVER']):
    '''
    Creates API blueprint with injected Objects.
    Must contain a sessionmanager and others.
    Always speaks OCPI 2.2

    Parameters
    ----------
    injected_objects : TYPE
        DESCRIPTION.

    Returns
    -------
    blueprint

    '''
    roles = [r.upper() for r in roles]
    blueprint = Blueprint("ocpi_api", __name__, url_prefix="/ocpi/v2")
    authorizations = {"Bearer": {"type": "apiKey",
                                 "in": "header", "name": "Authorization"}}

    api = Api(
        blueprint,
        version="1.0",
        title="OCPI OpenAPI Documentation",
        description="Welcome to the OpenAPI documentation site!",
        doc="/ui",
        authorizations=authorizations,
        default="Project-Backend",
        default_label="Beschreibung der API für das App-Framework"
    )

    if 'credentials' not in injected_objects:
        raise Exception('a credentials_manager must be injected')
    SingleCredMan.setInstance(injected_objects['credentials'])

    ns_dict = {
        'locations': makeLocationNamespace(roles),
        'credentials': credentials_ns,
        'versions': versions_ns,
        'commands': commands_ns,
        'sessions': makeSessionNamespace(roles),
        'reservations': reservation_ns,
    }
    endpoint_list = injected_objects.keys()
    injected_objects['versions'] = VersionManager(base_url, endpoint_list)
    used_namespaces = list(map(ns_dict.get, endpoint_list))

    # setting custom Namespaces should work too
    #import numpy as np
    #used_namespaces = np.logical_or(used_namespaces,injected_objects.values())

    for namesp in used_namespaces:

        if namesp is not None:
            log.debug(namesp.name)
            for res in namesp.resources:
                res.kwargs['resource_class_kwargs'] = injected_objects
            api.add_namespace(namesp, path="/"+namesp.name)
    return blueprint