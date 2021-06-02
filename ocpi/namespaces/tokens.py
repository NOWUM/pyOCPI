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
from flask_restx.inputs import datetime_from_iso8601
from ocpi.models import resp, respList
from ocpi.decorators import get_header_parser, token_required
from ocpi.models.tokens import add_models_to_tokens_namespace, Token, LocationReferences, AuthorizationInfo
from datetime import datetime


tokens_ns = Namespace(name="tokens", validate=True)

add_models_to_tokens_namespace(tokens_ns)
parser = get_header_parser(tokens_ns)

log = logging.getLogger('ocpi')

#TODO: Sender part vollständig?

def receiver():
    @tokens_ns.route('/<string:country_code>/<string:party_id>/<string:token_uid>')
    @tokens_ns.expect(parser)
    class manage_tokens(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.tokensmanager = kwargs['tokens_manager']
            super().__init__(api, *args, **kwargs)

        @tokens_ns.doc(params={
            'type': {'in': 'query', 'description': '', 'default': '', 'required': False}
        })

        @tokens_ns.marshal_with(resp(tokens_ns, Token))
        def get(self, country_code, party_id, token_uid):
            '''
            Retrieve a Token as it is stored in the CPO system.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('type', type=str)
            args = parser.parse_args()

            data = self.tokensmanager.getToken(country_code, party_id, token_uid, args['type'])
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        @tokens_ns.expect(Token) # New or updated Token object. --> expected Type in Request Body
        @tokens_ns.marshal_with(resp(tokens_ns, Token))
        def put(self, country_code, party_id, token_uid, type=None):
            '''
            Push new/updated Token object to the CPO.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('type', type=str)
            args = parser.parse_args()
            self.tokensmanager.putToken(country_code, party_id, token_uid, tokens_ns.payload, args['type'])
            data = 'accepted'
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }


        @tokens_ns.expect(Token)
        @tokens_ns.marshal_with(resp(tokens_ns, Token))
        def patch(self, country_code, party_id, token_uid, type=None):
            '''
            Notify the CPO of partial updates to a Token.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('type', type=str)
            args = parser.parse_args()
            self.tokensmanager.patchToken(country_code, party_id, token_uid, tokens_ns.payload, args['type'])
            data = 'accepted'
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

    return tokens_ns


def sender():
    # TODO: add sender endpoints
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
        @token_required #TODO: wird diese Zeile hier benötigt?
        def get(self):
            '''
            Get Tokens, allows pagination
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('from', type=datetime_from_iso8601)
            parser.add_argument('to', type=datetime_from_iso8601)
            parser.add_argument('offset', type=int)
            parser.add_argument('limit', type=int)
            args = parser.parse_args()

            data = self.tokensmanager.getTokens(
                args['from'], args['to'], args['offset'], args['limit'])
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }


    @tokens_ns.route('/<string:token_uid>/authorize')
    @tokens_ns.expect(parser)
    class validate_token(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.tokensmanager = kwargs['tokens_manager']
            super().__init__(api, *args, **kwargs)

        @tokens_ns.expect(LocationReferences) #<--  Optional Request Body TODO: is it optinal like this?
        @tokens_ns.marshal_with(resp(tokens_ns, Token))
        def post(self, token_uid):
            parser = reqparse.RequestParser()
            parser.add_argument('type', type=str)
            args = parser.parse_args()

            #TODO check logic, add AuthorizationInfo Object:
            #When the token is known by the Sender, the response SHALL contain a AuthorizationInfo object.
            if token_uid in self.tokensmanager.tokens.keys():
                data=None
                #data = AuthorizationInfo #TODO: get AuthorizationInfo Object
                return {'data': data,
                        'status_code': 1000,
                        'status_message': 'nothing',
                        'timestamp': datetime.now()
                        }
            # If the token is not known, the response SHALL contain the status code: 2004: Unknown Token, and no data field.
            else:
                return {'data': None,
                        'status_code': 2004,
                        'status_message': 'Unknown Token',
                        'timestamp': datetime.now()
                        }

    return tokens_ns


def makeTokenNamespace(interfaces=['SENDER', 'RECEIVER']):
    log.debug('tokens interfaces:'+str(interfaces))
    if 'SENDER' in interfaces:
        sender()
    if 'RECEIVER' in interfaces:
        receiver()

    return tokens_ns
