#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:32:01 2021

@author: maurer
"""

from flask_restx import Resource, Namespace, fields
from flask_restx.inputs import datetime_from_iso8601
from ocpi.models.sessions import add_models_to_session_namespace, Session, ChargingPreferences, charging_pref_results
from flask_restx import reqparse
from ocpi.models import resp, respList
from ocpi.decorators import get_header_parser, token_required

sessions_ns = Namespace(name="sessions", validate=True)
add_models_to_session_namespace(sessions_ns)
header_parser = get_header_parser(sessions_ns)


def senderNamespace():
    @sessions_ns.route('/', doc={"description": "API Endpoint for Session management"})
    @sessions_ns.expect(header_parser)
    class get_sessions(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.sessionmanager = kwargs['sessions']
            super().__init__(api, *args, **kwargs)

        @sessions_ns.doc(params={
            'from': {'in': 'query', 'description': 'declare session start point', 'default': '2021-01-01T13:30:00+02:00', 'required': True},
            'to': {'in': 'query', 'description': 'declare session end point', 'default': '2021-01-01T15:30:00+02:00', 'required': True},
            'offset': {'in': 'query', 'description': 'id offset for pagination', 'default': '0'},
            'limit': {'in': 'query', 'description': 'number of entries to get', 'default': '50'},

        })
        @sessions_ns.marshal_with(respList(sessions_ns, Session))
        @token_required
        def get(self):
            '''
            Only Sessions with last_update between the given {date_from} (including) and {date_to} (excluding) will be returned.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('from', type=datetime_from_iso8601)
            parser.add_argument('to', type=datetime_from_iso8601)
            parser.add_argument('offset', type=int)
            parser.add_argument('limit', type=int)
            args = parser.parse_args()
            return self.sessionmanager.getSessions(args['from'], args['to'], args['offset'], args['limit'])

    @sessions_ns.route('/<string:session_id>/charging_preferences', doc={"description": "OCPI ChargingPreferences"})
    @sessions_ns.response(404, 'SessionID not found')
    @sessions_ns.expect(header_parser)
    class charging_preferences(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.sessionmanager = kwargs['sessions']
            super().__init__(api, *args, **kwargs)

        @sessions_ns.doc('PutCommand')
        @sessions_ns.expect(ChargingPreferences)
        @sessions_ns.marshal_with(fields.String(enum=charging_pref_results), code=201)
        @sessions_ns.response(404, 'EVSE not capable of smartcharging')
        @token_required
        def put(self, session_id):
            '''Update ChargingPreferences'''
            session_id = session_id.lower()  # caseinsensitive

            return self.sessionmanager.updateChargingPrefs(session_id, sessions_ns.payload)
            # TODO save and process preferences somewhere
    return sessions_ns


def receiverNamespace():
    @sessions_ns.route('/<string:country_id>/<string:party_id>/<string:session_id>', doc={"description": "API Endpoint for Session management"})
    @sessions_ns.response(404, 'Command not found')
    @sessions_ns.expect(header_parser)
    class receiver_session(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.session_manager = kwargs['sessions']
            super().__init__(api, *args, **kwargs)

        @sessions_ns.marshal_with(resp(sessions_ns, Session), code=200)
        @token_required
        def get(self, country_id, party_id, session_id):

            # TODO validate country and party
            return self.session_manager.getSession(country_id, party_id, session_id)

        @sessions_ns.expect(Session)
        @sessions_ns.marshal_with(resp(sessions_ns, Session), code=201)
        @token_required
        def put(self, country_id, party_id, session_id):
            '''Add new Session'''
            session_id = session_id.lower()  # caseinsensitive
            country_id = country_id.lower()
            party_id = party_id.lower()

            return self.session_manager.createSession(country_id, party_id, sessions_ns.payload)

        @sessions_ns.expect(Session, validate=False)
        @sessions_ns.marshal_with(resp(sessions_ns, Session), code=201)
        @token_required
        def patch(self, country_id, party_id, session_id):
            session_id = session_id.lower()  # caseinsensitive
            country_id = country_id.lower()
            party_id = party_id.lower()

            return self.session_manager.patchSession(country_id, party_id, session_id, sessions_ns.payload)
            # TODO save and process preferences somewhere
    return sessions_ns


def makeSessionNamespace(interfaces=['SENDER', 'RECEIVER']):
    if 'SENDER' in interfaces:
        senderNamespace()
    if 'RECEIVER' in interfaces:
        receiverNamespace()
    return sessions_ns