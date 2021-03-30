#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 18:26:15 2021

@author: maurer
"""

from flask_restx import Resource, Namespace
from ocpi.models.location import add_models_to_location_namespace, EVSE, Location
from flask_restx import reqparse
from flask_restx.inputs import datetime_from_iso8601

locations_ns = Namespace(name="locations", validate=True)

add_models_to_location_namespace(locations_ns)



@locations_ns.route('/', doc={"description": "API Endpoint for Session management"})
class get_session(Resource):

    def __init__(self, api=None, *args, **kwargs):
        # sessions is a black box dependency
        self.sessionmanager = kwargs['session_manager']
        super().__init__(api, *args, **kwargs)

    @locations_ns.doc(params={
        'from': {'in': 'query', 'description': 'declare session start point', 'default': '2021-01-01T13:30:00+02:00', 'required': True},
        'to': {'in': 'query', 'description': 'declare session end point', 'default': '2021-01-01T15:30:00+02:00', 'required': True},
        'offset': {'in': 'query', 'description': 'id offset for pagination', 'default': '0'},
        'limit': {'in': 'query', 'description': 'number of entries to get', 'default': '50'},

    })
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

@locations_ns.route('/START_SESSION', doc={"description": "OCPI Command API"},)
@locations_ns.response(404, 'Command not found')
class start_session(Resource):
    @locations_ns.doc('PostCommand')  # operationId
    def post(self):
        '''Start Charging Session'''
        # return resMan.create(api.payload), 201
        pass


@locations_ns.route('/STOP_SESSION', doc={"description": "OCPI Command API"},)
@locations_ns.response(404, 'Command not found')
class stop_session(Resource):
    @locations_ns.expect(EVSE)
    def post(self):
        '''Stop Charging Session'''
        # return resMan.create(api.payload), 201
        pass


@locations_ns.route('/UNLOCK_CONNECTOR', doc={"description": "OCPI Command API"},)
@locations_ns.response(404, 'Command not found')
class unlock_connector(Resource):
    @locations_ns.expect(Location)
    def post(self):
        '''Unlock Connector'''
        # return resMan.create(api.payload), 201
        pass


@locations_ns.route('/CANCEL_RESERVATION', doc={"description": "OCPI Command API"},)
@locations_ns.response(404, 'Command not found')
class cancel_reservation(Resource):
    def post(self):
        '''cancel reservation'''
        # return resMan.create(api.payload), 201
        pass


@locations_ns.route('/RESERVE_NOW', doc={"description": "OCPI Command API"},)
@locations_ns.response(404, 'Command not found')
class resrve_now(Resource):
    def post(self):
        '''resrve Now'''
        # return resMan.create(api.payload), 201
        pass