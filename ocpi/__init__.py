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
from ocpi.namespaces.sessions import sessions_ns
from ocpi.namespaces.locations import locations_ns
from ocpi.namespaces.versions import versions_ns
from ocpi.namespaces.credentials import credentials_ns
from ocpi.decorators import SingleCredMan


def createOcpiBlueprint(injected_objects,namespaces=[versions_ns, credentials_ns, commands_ns, sessions_ns, locations_ns]):
    '''
    Creates API blueprint with injected Objects.
    Must contain a sessionmanager and others

    Parameters
    ----------
    injected_objects : TYPE
        DESCRIPTION.

    Returns
    -------
    blueprint

    '''
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

    if 'credentials_manager' not in injected_objects:
        raise Exception('a credentials_manager must be injected')
    SingleCredMan.setInstance(injected_objects['credentials_manager'])

    for namesp in namespaces:
        for res in namesp.resources:
            res.kwargs['resource_class_kwargs'] = injected_objects
        api.add_namespace(namesp, path="/"+namesp.name)
    return blueprint