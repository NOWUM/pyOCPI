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
    'credentials': {'role': 'SENDER', 'object': None},
    'locations': {'role': 'SENDER', 'object': None},
    'versions': {'role': 'SENDER', 'object': None},
    'commands': {'role': 'SENDER', 'object': None},
    'sessions': {'role': 'SENDER', 'object': None},
    'reservations': {'role': 'SENDER', 'object': None},
}


def createOcpiBlueprint(base_url, injected_objects=injected, ocpi_version='2.2'):
    '''
    Creates API blueprint with injected Objects.
    Must contain a sessionmanager and others.
    Always speaks OCPI 2.2

    Parameters
    ----------
    injected_objects : dict
        DESCRIPTION.

    Returns
    -------
    blueprint

    '''
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
    SingleCredMan.setInstance(injected_objects['credentials']['object'])

    ns_dict = {
        'locations': makeLocationNamespace,
        'credentials': lambda x: credentials_ns,
        'versions': lambda x: versions_ns,
        'commands': makeCommandsNamespace,
        'sessions': makeSessionNamespace,
        'reservations': makeReservationNamespace,
        'parking': makeParkingNamespace,
        'charging_profiles': makeChargingProfilesNamespace,
        'tokens': makeTokenNamespace,
        'tariffs': makeTariffsNamespace,
        'cdrs': makeCdrNamespace,
    }

    used_namespaces = []
    inj_obj = {}
    endpoints = {}
    for key, value in injected_objects.items():
        ns = ns_dict[key](value['role'].upper())
        used_namespaces.append(ns)

        inj_obj[key] = value['object']
        endpoints[key] = value['role'].upper()

    inj_obj['versions'] = VersionManager(
        base_url, endpoints, ocpi_version)

    # setting custom Namespaces should work too
    #import numpy as np
    #used_namespaces = np.logical_or(used_namespaces,inj_obj.values())

    log.debug(list(map(lambda x: x.name if x else '', used_namespaces)))

    # versions endpoint doe not include version
    for res in versions_ns.resources:
        res.kwargs['resource_class_kwargs'] = inj_obj
    api.add_namespace(versions_ns, path="/")

    for namesp in used_namespaces:
        if namesp is not None:
            for res in namesp.resources:
                res.kwargs['resource_class_kwargs'] = inj_obj
            api.add_namespace(namesp, path=f"/{ocpi_version}/"+namesp.name)
    return blueprint