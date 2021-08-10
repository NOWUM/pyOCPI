#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:03:00 2021
https://github.com/ocpi/ocpi/blob/master/mod_tokens.asciidoc
@author: gruell
"""

import logging
from flask_restx import Resource, Namespace
from flask_restx import reqparse
from ocpi.models import resp, respList
from ocpi.namespaces import (get_header_parser, token_required,
                             pagination_parser, make_response)
from ocpi.models.tokens import add_models_to_tokens_namespace, Token, LocationReferences

tokens_ns = Namespace(name="tokens", validate=True)

add_models_to_tokens_namespace(tokens_ns)
parser = get_header_parser(tokens_ns)

log = logging.getLogger('ocpi')


def receiver():
    @tokens_ns.route('/<string:country_code>/<string:party_id>/<string:token_uid>')
    @tokens_ns.expect(parser)
    class manage_tokens(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.tokensmanager = kwargs['tokens']
            super().__init__(api, *args, **kwargs)

        @tokens_ns.doc(params={
            'type': {'in': 'query', 'description': '', 'default': '', 'required': False}
        })
        @tokens_ns.marshal_with(resp(tokens_ns, Token))
        @token_required
        def get(self, country_code, party_id, token_uid):
            '''
            Retrieve a Token as it is stored in the CPO system.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('type', type=str)
            args = parser.parse_args()

            return make_response(self.tokensmanager.getToken,
                                 country_code, party_id, token_uid, args.get('type'))

        # New or updated Token object. --> expected Type in Request Body
        @tokens_ns.expect(Token)
        @tokens_ns.marshal_with(resp(tokens_ns, Token))
        @token_required
        def put(self, country_code, party_id, token_uid, type=None):
            '''
            Push new/updated Token object to the CPO.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('type', type=str)
            args = parser.parse_args()
            return make_response(self.tokensmanager.putToken,
                                 country_code, party_id, token_uid,
                                 tokens_ns.payload, args.get('type'))

        @tokens_ns.expect(Token)
        @tokens_ns.marshal_with(resp(tokens_ns, Token))
        @token_required
        def patch(self, country_code, party_id, token_uid, type=None):
            '''
            Notify the CPO of partial updates to a Token.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('type', type=str)
            args = parser.parse_args()
            return make_response(self.tokensmanager.patchToken,
                                 country_code, party_id, token_uid, tokens_ns.payload, args.get('type'))

    return tokens_ns


def sender():
    @tokens_ns.route('/', doc={"description": "API Endpoint for Tokens management"})
    @tokens_ns.expect(parser)
    class get_tokens(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.tokensmanager = kwargs['tokens']
            super().__init__(api, *args, **kwargs)

        @tokens_ns.doc(params={
            'date_from': {'in': 'query', 'description': 'Only return Tokens that have last_updated after or equal to this Date/Time (inclusive).',
                          'default': '2021-01-01T13:30:00+02:00', 'required': True},
            'date_to': {'in': 'query', 'description': 'Only return Tokens that have last_updated up to this Date/Time, but not including (exclusive).', 'default': '2038-01-01T15:30:00+02:00',
                        'required': True},
            'offset': {'in': 'query', 'description': 'The offset of the first object returned. Default is 0.', 'default': '0'},
            'limit': {'in': 'query', 'description': 'Maximum number of objects to GET.', 'default': '50'},
        })
        @tokens_ns.marshal_with(respList(tokens_ns, Token))
        @token_required
        def get(self):
            '''
            Get the list of known Tokens, last updated between the {date_from} and {date_to} (paginated)
            '''
            parser = pagination_parser()
            args = parser.parse_args()

            return make_response(self.tokensmanager.getTokens,
                                 args['from'], args['to'], args['offset'], args['limit'])

    @tokens_ns.route('/<string:token_uid>/authorize')
    @tokens_ns.expect(parser)
    class validate_token(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.tokensmanager = kwargs['tokens']
            super().__init__(api, *args, **kwargs)

        @tokens_ns.expect(LocationReferences)
        @tokens_ns.marshal_with(resp(tokens_ns, Token))
        @token_required
        def post(self, token_uid):
            parser = reqparse.RequestParser()
            parser.add_argument('type', type=str, default=None)
            args = parser.parse_args()

            return make_response(self.tokensmanager.validateToken,
                                 token_uid, args.get('type'), tokens_ns.payload)

    return tokens_ns


def makeTokenNamespace(role):
    if role == 'SENDER':
        sender()
    elif role == 'RECEIVER':
        receiver()
    else:
        raise Exception('invalid role')

    return tokens_ns