#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:45:34 2021

@author: maurer
"""

from werkzeug.exceptions import BadRequest
from ocpi.decorators import token_required, get_header_parser, _check_access_token
from flask_restx import Resource, Namespace
from ocpi.models.credentials import Credentials, add_models_to_credentials_namespace
from ocpi.models import resp
from datetime import datetime
from ocpi.managers import CredentialsManager
credentials_ns = Namespace(name="credentials", validate=True)
add_models_to_credentials_namespace(credentials_ns)
parser = get_header_parser(credentials_ns)


@credentials_ns.route('/', doc={"description": "API Endpoint for Session management"})
@credentials_ns.response(405, 'method not allowed')
@credentials_ns.response(401, 'unauthorized')
class credentials(Resource):

    def __init__(self, api=None, *args, **kwargs):
        # type: CredentialsManager
        self.credentials_manager = kwargs['credentials']
        super().__init__(api, *args, **kwargs)

    @token_required
    @credentials_ns.marshal_with(resp(credentials_ns, Credentials))
    @credentials_ns.expect(parser)
    def get(self):
        '''
        request the credentials object if authenticated
        '''
        decodedToken = _check_access_token()
        data = self.credentials_manager.getCredentials(decodedToken)
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }

    @token_required
    @credentials_ns.marshal_with(resp(credentials_ns, Credentials))
    @credentials_ns.expect(parser, Credentials)
    def post(self):
        '''
        Get new Token, request Sender Token and reply with Token C (for first time auth)
        '''
        try:

            decodedToken = _check_access_token()
        except:
            raise BadRequest('Authorization Header must be base64 encoded')
        data = self.credentials_manager.makeRegistration(
            credentials_ns.payload, decodedToken)
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }

    @token_required
    @credentials_ns.marshal_with(resp(credentials_ns, Credentials))
    @credentials_ns.expect(parser, Credentials)
    def put(self):
        '''
        replace registration Token for version update
        '''
        decodedToken = _check_access_token()
        data = self.credentials_manager.versionUpdate(
            credentials_ns.payload, decodedToken)
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }

    @token_required
    @credentials_ns.expect(parser)
    def delete(self):
        '''
        unregisters from server
        '''
        decodedToken = _check_access_token()
        data = self.credentials_manager.unregister(decodedToken)
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }