#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 22:48:06 2021

@author: maurer
"""

from flask_restx import Resource, Namespace
from ocpi.models.version import VersionDetailsData, VersionsData, add_models_to_version_namespace
from ocpi.decorators import get_header_parser

versions_ns = Namespace(name="versions", validate=True)
add_models_to_version_namespace(versions_ns)
header_parser = get_header_parser(versions_ns)


@versions_ns.route('/', doc={"description": "API Endpoint for Session management"})
class get_versions(Resource):

    def __init__(self, api=None, *args, **kwargs):
        self.versionsmanager = kwargs['versions']
        super().__init__(api, *args, **kwargs)

    @versions_ns.marshal_with(VersionsData)
    def get(self):
        return self.versionsmanager.versions()


@versions_ns.route('/details', doc={"description": "API Endpoint for Session management"})
class get_details(Resource):

    def __init__(self, api=None, *args, **kwargs):
        self.versionsmanager = kwargs['versions']
        super().__init__(api, *args, **kwargs)

    @versions_ns.marshal_with(VersionDetailsData)
    def get(self):
        '''
        Get Version Details
        '''

        return self.versionsmanager.details()