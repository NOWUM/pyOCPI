#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 22:48:06 2021

@author: maurer
"""

from flask_restx import Resource, Namespace
from ocpi.models.version import VersionDetailsData, VersionsData, add_models_to_version_namespace

versions_ns = Namespace(name="versions", validate=True)

add_models_to_version_namespace(versions_ns)


@versions_ns.route('/', doc={"description": "API Endpoint for Session management"})
class get_versions(Resource):

    def __init__(self, api=None, *args, **kwargs):
        # sessions is a black box dependency
        self.versionsmanager = kwargs['session_manager']
        super().__init__(api, *args, **kwargs)

    @versions_ns.marshal_with(VersionsData)
    def get(self):
        return {'versions': [
            {'version': '2.2', 'url': 'http://localhost:5000/ocpi/v2'}]}


@versions_ns.route('/details', doc={"description": "API Endpoint for Session management"})
class get_details(Resource):

    def __init__(self, api=None, *args, **kwargs):
        # sessions is a black box dependency
        self.versionsmanager = kwargs['session_manager']
        super().__init__(api, *args, **kwargs)

    @versions_ns.marshal_with(VersionDetailsData)
    def get(self):
        '''
        Get Version Details
        '''

        return {'version': '2.2', 'endpoints': [
            {'identifier': 'commands', 'url': 'http://localhost:5000/ocpi/v2/commands/'},
            {'identifier': 'locations',
                'url': 'http://localhost:5000/ocpi/v2/locations/'},
            {'identifier': 'sessions', 'url': 'http://localhost:5000/ocpi/v2/sessions/'}]}