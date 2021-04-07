#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 18:26:15 2021

@author: maurer
"""

from flask_restx import Resource, Namespace
from ocpi.models.location import add_models_to_location_namespace, EVSE, Location, Connector
from flask_restx import reqparse
from flask_restx.inputs import datetime_from_iso8601

locations_ns = Namespace(name="locations", validate=True)

add_models_to_location_namespace(locations_ns)


@locations_ns.route('/', doc={"description": "API Endpoint for Locations management"})
class get_locations(Resource):

    def __init__(self, api=None, *args, **kwargs):
        self.locationmanager = kwargs['location_manager']
        super().__init__(api, *args, **kwargs)

    @locations_ns.doc(params={
        'from': {'in': 'query', 'description': 'declare session start point', 'default': '2021-01-01T13:30:00+02:00', 'required': True},
        'to': {'in': 'query', 'description': 'declare session end point', 'default': '2021-01-01T15:30:00+02:00', 'required': True},
        'offset': {'in': 'query', 'description': 'id offset for pagination', 'default': '0'},
        'limit': {'in': 'query', 'description': 'number of entries to get', 'default': '50'},

    })
    @locations_ns.marshal_with(Location)
    def get(self):
        '''
        Get Location, allows pagination
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=datetime_from_iso8601)
        parser.add_argument('to', type=datetime_from_iso8601)
        parser.add_argument('offset', type=int)
        parser.add_argument('limit', type=int)
        args = parser.parse_args()

        return list(self.locationmanager.sessions.values())[args['offset']:args['offset']+args['limit']]


# keep in mind: https://stackoverflow.com/a/16569475
@locations_ns.route('/<string:location_id>',
                    '/<string:location_id>/<string:evse_uid>',
                    '/<string:location_id>/<string:evse_uid>/<string:connector_id>')
class get_location(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.locationmanager = kwargs['location_manager']
        super().__init__(api, *args, **kwargs)

    def get(self, location_id, evse_uid=None, connector_id=None):
        '''
        Filter Locations/EVSEs/Connectors by id
        '''

        return self.locationmanager.sessions[location_id]

# Receiver interface: eMSP and NSP.


@locations_ns.route('/<string:country_code>/<string:party_id>/<string:location_id>')
class manage_location(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.locationmanager = kwargs['location_manager']
        super().__init__(api, *args, **kwargs)

    @locations_ns.marshal_with(Location)
    def get(self, country_code, party_id, location_id):
        '''
        Get Location by ID
        '''

        return self.locationmanager.sessions[location_id]

    @locations_ns.expect(Location)
    @locations_ns.marshal_with(Location)
    def put(self, country_code, party_id, location_id):
        '''
        Add/Replace Location by ID
        '''

        return self.locationmanager.sessions[location_id]

    @locations_ns.expect(Location)
    @locations_ns.marshal_with(Location)
    def patch(self, country_code, party_id, location_id):
        '''
        Partially update Location
        '''

        return self.locationmanager.sessions[location_id]


@locations_ns.route('/<string:country_code>/<string:party_id>/<string:location_id>/<string:evse_uid>')
class manage_evse(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.locationmanager = kwargs['location_manager']
        super().__init__(api, *args, **kwargs)

    @locations_ns.marshal_with(EVSE)
    def get(self, country_code, party_id, location_id, evse_uid):
        '''
        Get EVSE by ID
        '''

        return self.locationmanager.sessions[location_id][evse_uid]

    @locations_ns.expect(EVSE)
    @locations_ns.marshal_with(EVSE)
    def put(self, country_code, party_id, location_id, evse_uid):
        '''
        Add/Replace EVSE by ID
        '''

        return self.locationmanager.sessions[location_id][evse_uid]

    @locations_ns.expect(EVSE)
    @locations_ns.marshal_with(EVSE)
    def patch(self, country_code, party_id, location_id, evse_uid):
        '''
        Partially update EVSE
        '''

        return self.locationmanager.sessions[location_id][evse_uid]


@locations_ns.route('/<string:country_code>/<string:party_id>/<string:location_id>/<string:evse_uid>/<string:connector_id>')
class manage_connector(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.locationmanager = kwargs['location_manager']
        super().__init__(api, *args, **kwargs)

    @locations_ns.marshal_with(Connector)
    def get(self, country_code, party_id, location_id, evse_uid, connector_id):
        '''
        Get Connector by ID
        '''

        return self.locationmanager.sessions[location_id][evse_uid][connector_id]

    @locations_ns.expect(Connector)
    @locations_ns.marshal_with(Connector)
    def put(self, country_code, party_id, location_id, evse_uid):
        '''
        Add/Replace Connector by ID
        '''

        return self.locationmanager.sessions[location_id][evse_uid]

    @locations_ns.expect(Connector)
    @locations_ns.marshal_with(Connector)
    def patch(self, country_code, party_id, location_id, evse_uid):
        '''
        Partially update Connector
        '''

        return self.locationmanager.sessions[location_id][evse_uid]
