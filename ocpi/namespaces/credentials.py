#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:45:34 2021

@author: maurer
"""

from ocpi.decorators import token_required
from flask_restx import Resource, Namespace
from ocpi.models.credentials import Credentials, add_models_to_credentials_namespace

credentials_ns = Namespace(name="credentials", validate=True)
add_models_to_credentials_namespace(credentials_ns)


parser = credentials_ns.parser()
parser.add_argument('Authorization', location='headers', required=True)


@credentials_ns.route('/', doc={"description": "API Endpoint for Session management"})
@credentials_ns.response(405, 'method not allowed')
@credentials_ns.response(401, 'unauthorized')
class credentials(Resource):

    def __init__(self, api=None, *args, **kwargs):
        # sessions is a black box dependency
        self.credentials_manager = kwargs['credentials_manager']
        super().__init__(api, *args, **kwargs)

    @credentials_ns.marshal_with(Credentials)
    def get(self):
        '''
        request new credentials if authenticated
        '''
        return self.credentials_manager.createCredentials()

    @credentials_ns.marshal_with(Credentials)
    @credentials_ns.expect(parser)
    @token_required
    def post(self):
        '''
        Get new Token, request Sender Token and reply with Token C (for first time auth)
        '''
        return self.credentials_manager.updateRegistration(credentials_ns.payload)

    @token_required
    @credentials_ns.marshal_with(Credentials)
    @credentials_ns.expect(parser)
    def put(self):
        '''
        replace registration Token
        '''
        return self.credentials_manager.replaceToken(credentials_ns.payload)

    @token_required
    @credentials_ns.marshal_with(Credentials)
    @credentials_ns.expect(parser)
    def delete(self):
        '''
        unregisters from server
        '''
        credentials_ns.payloadload
        return self.credentials_manager.removeToken(credentials_ns.payload)