#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 22:48:06 2021

@author: maurer
"""

from flask_restx import Resource, Namespace
from ocpi.models.version import VersionDetailsData, VersionsData, add_models_to_version_namespace
from ocpi.decorators import get_header_parser
from ocpi.models import resp
from datetime import datetime

versions_ns = Namespace(name="versions", validate=True)
add_models_to_version_namespace(versions_ns)
header_parser = get_header_parser(versions_ns)


@versions_ns.route('/', doc={"description": "API Endpoint for Session management"})
class get_versions(Resource):

    def __init__(self, api=None, *args, **kwargs):
        self.versionsmanager = kwargs['versions']
        super().__init__(api, *args, **kwargs)

    @versions_ns.marshal_with(resp(versions_ns, VersionsData))
    def get(self):
        data = self.versionsmanager.versions()
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }


@versions_ns.route('/details', doc={"description": "API Endpoint for Session management"})
class get_details(Resource):

    def __init__(self, api=None, *args, **kwargs):
        self.versionsmanager = kwargs['versions']
        super().__init__(api, *args, **kwargs)

    @versions_ns.marshal_with(resp(versions_ns, VersionDetailsData))
    def get(self):
        '''
        Get Version Details
        '''

        data = self.versionsmanager.details()
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }