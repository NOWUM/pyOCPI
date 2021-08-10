#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 18:02:46 2021

@author: maurer

Api definition file
"""

from flask import Blueprint
from flask_restx import Api

from ocpi.namespaces.versions import versions_ns
from ocpi.namespaces.credentials import credentials_ns
from ocpi.namespaces.commands import makeCommandsNamespace
from ocpi.namespaces.sessions import makeSessionNamespace
from ocpi.namespaces.locations import makeLocationNamespace
from ocpi.namespaces.reservation import makeReservationNamespace
from ocpi.namespaces.parking import makeParkingNamespace
from ocpi.namespaces.tokens import makeTokenNamespace
from ocpi.namespaces.cdrs import makeCdrNamespace
from ocpi.namespaces.tariffs import makeTariffsNamespace
from ocpi.namespaces.charging_profiles import makeChargingProfilesNamespace
from ocpi.namespaces import SingleCredMan
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

def createOcpiBlueprint(base_url, injected_objects=injected, roles=['CPO','SENDER', 'RECEIVER'], ocpi_version='2.2'):
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
    blueprint = Blueprint("ocpi_api", __name__, url_prefix="/ocpi")
    authorizations = {"Bearer": {"type": "apiKey",
                                 "in": "header", "name": "Authorization"}}

    api = Api(
        blueprint,
        version=ocpi_version,
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
        'commands': makeCommandsNamespace(roles),
        'sessions': makeSessionNamespace(roles),
        'reservations': makeReservationNamespace(roles),
        'parking': makeParkingNamespace(roles),
        'charging_profiles': makeChargingProfilesNamespace(roles),
        'tokens': makeTokenNamespace(roles),
        'tariffs': makeTariffsNamespace(roles),
        'cdrs': makeCdrNamespace(roles),
    }

    endpoint_list = injected_objects.keys()
    used_namespaces = list(map(ns_dict.get, endpoint_list))
    injected_objects['versions'] = VersionManager(base_url, endpoint_list, ['SENDER'], ocpi_version)


    # setting custom Namespaces should work too
    #import numpy as np
    #used_namespaces = np.logical_or(used_namespaces,injected_objects.values())

    log.debug(list(map(lambda x: x.name if x else '', used_namespaces)))

    # versions endpoint doe not include version
    for res in versions_ns.resources:
            res.kwargs['resource_class_kwargs'] = injected_objects
    api.add_namespace(versions_ns, path="/")

    for namesp in used_namespaces:

        if namesp is not None:
            for res in namesp.resources:
                res.kwargs['resource_class_kwargs'] = injected_objects
            api.add_namespace(namesp, path=f"/{ocpi_version}/"+namesp.name)
    return blueprint