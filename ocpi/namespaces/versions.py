#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 22:48:06 2021

@author: maurer
"""

from flask_restx import Resource, Namespace
from ocpi.models.version import VersionDetailsData, VersionsData, add_models_to_version_namespace
from ocpi.namespaces import get_header_parser, make_response
from ocpi.models import resp

versions_ns = Namespace(name="versions", validate=True)
add_models_to_version_namespace(versions_ns)
header_parser = get_header_parser(versions_ns)


@versions_ns.route('versions', doc={"description": "API Endpoint to get available versions"})
class get_versions(Resource):

    def __init__(self, api=None, *args, **kwargs):
        self.versionsmanager = kwargs['versions']
        super().__init__(api, *args, **kwargs)

    @versions_ns.marshal_with(resp(versions_ns, VersionsData))
    def get(self):
        return make_response(self.versionsmanager.versions)

# TODO flexible version number for OCPI 3.x
@versions_ns.route('2.2', doc={"description": "API Endpoint for Version details"})
class get_details(Resource):

    def __init__(self, api=None, *args, **kwargs):
        self.versionsmanager = kwargs['versions']
        super().__init__(api, *args, **kwargs)

    @versions_ns.marshal_with(resp(versions_ns, VersionDetailsData))
    def get(self):
        '''
        Get Version Details
        '''

        return make_response(self.versionsmanager.details)