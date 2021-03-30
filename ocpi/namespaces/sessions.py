#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:32:01 2021

@author: maurer
"""

from flask_restx import Resource, Namespace
from flask_restx.inputs import datetime_from_iso8601
from ocpi.models.sessions import add_models_to_session_namespace, Session, ChargingPreferences
from flask_restx import reqparse

sessions_ns = Namespace(name="sessions", validate=True)
add_models_to_session_namespace(sessions_ns)


@sessions_ns.route('/', doc={"description": "API Endpoint for Session management"})
class get_session(Resource):

    def __init__(self, api=None, *args, **kwargs):
        # sessions is a black box dependency
        self.sessionmanager = kwargs['session_manager']
        super().__init__(api, *args, **kwargs)

    @sessions_ns.doc(params={
        'from': {'in': 'query', 'description': 'declare session start point', 'default': '2021-01-01T13:30:00+02:00', 'required': True},
        'to': {'in': 'query', 'description': 'declare session end point', 'default': '2021-01-01T15:30:00+02:00', 'required': True},
        'offset': {'in': 'query', 'description': 'id offset for pagination', 'default': '0'},
        'limit': {'in': 'query', 'description': 'number of entries to get', 'default': '50'},

    })
    @sessions_ns.marshal_with(Session)
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

        return list(self.sessionmanager.sessions.values())[args['offset']:args['offset']+args['limit']]


charging_pref_results = ["ACCEPTED", "DEPARTURE_REQUIRED",
                         "ENERGY_NEED_REQUIRED", "NOT_POSSIBLE", "PROFILE_TYPE_NOT_SUPPORTED"]

charging_prefs = {}


@sessions_ns.route('/<string:session_id>/charging_preferences', doc={"description": "OCPI CharginPreferences"})
@sessions_ns.response(404, 'SessionID not found')
class charging_preferences(Resource):

    def __init__(self, api=None, *args, **kwargs):
        # sessions is a black box dependency
        self.sessionmanager = kwargs['session_manager']
        super().__init__(api, *args, **kwargs)

    @sessions_ns.doc('PutCommand')
    @sessions_ns.expect(ChargingPreferences)
    @sessions_ns.marshal_with(ChargingPreferences, code=201)
    def put(self, session_id):
        '''Update ChargingPreferences'''
        session_id = session_id.lower()  # caseinsensitive
        try:
            self.sessionmanager.sessions[session_id]['preferences'] = sessions_ns.payload
        except:
            return '', 404
        # TODO save and process preferences somewhere

        return session_id, 201

    @sessions_ns.doc('PatchCommand')
    @sessions_ns.expect(ChargingPreferences)
    @sessions_ns.marshal_with(ChargingPreferences, code=201)
    def patch(self, session_id):
        '''Update ChargingPreferences'''
        session_id = session_id.lower()  # caseinsensitive
        try:
            self.sessionmanager.sessions[session_id]['preferences'].update(
                sessions_ns.payload)
        except:
            return '', 404
        # TODO save and process preferences somewhere

        return session_id, 200


@sessions_ns.route('/<string:country_id>/<string:party_id>/<string:session_id>', doc={"description": "API Endpoint for Session management"})
@sessions_ns.response(404, 'Command not found')
class start_session(Resource):

    def __init__(self, api=None, *args, **kwargs):
        # sessions is a black box dependency
        self.session_manager = kwargs['session_manager']
        super().__init__(api, *args, **kwargs)

    @sessions_ns.marshal_with(Session, code=200)
    @sessions_ns.marshal_with(str, code=404)
    def get(self, country_id, party_id, session_id):

        try:
            ses = self.session_manager.sessions[session_id]
            # TODO validate country and party
        except:
            return '', 404

        return ses

    @sessions_ns.expect(Session)
    @sessions_ns.marshal_with(Session, code=201)
    def put(self, country_id, party_id, session_id):
        '''Add new Session'''
        session_id = session_id.lower()  # caseinsensitive
        country_id = country_id.lower()
        party_id = party_id.lower()

        self.session_manager.sessions[session_id] = sessions_ns.payload
        self.session_manager.sessions[session_id]['country_id'] = country_id
        self.session_manager.sessions[session_id]['party_id'] = party_id
        # TODO save and process preferences somewhere

        return self.session_manager.sessions[session_id], 201