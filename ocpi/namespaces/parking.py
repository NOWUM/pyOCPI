#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 14:25:05 2021

@author: maurer

Custom module for parking spot management

parking service operator gets messages reservation requests and answers with price
reservations can be
"""

from flask_restx import Resource, Namespace
from ocpi.models import resp, respList
from ocpi.models.parking import add_models_to_parking_namespace, ParkingSession
from ocpi.namespaces import (get_header_parser, token_required,
                             pagination_parser, make_response)

parking_ns = Namespace(name="parking", validate=True)
add_models_to_parking_namespace(parking_ns)
header_parser = get_header_parser(parking_ns)


def sender():
    @parking_ns.route(
        "/", doc={"description": "API Endpoint for ParkingSession management"}
    )
    @parking_ns.expect(header_parser)
    class get_parking_sessions(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.parking_manager = kwargs["parking"]
            super().__init__(api, *args, **kwargs)

        @parking_ns.doc(params={
            'from': {'in': 'query', 'description': 'declare ParkingSession start point', 'default': '2021-01-01T13:30:00+02:00', 'required': True},
            'to': {'in': 'query', 'description': 'declare ParkingSession end point', 'default': '2038-01-01T15:30:00+02:00', 'required': True},
            'offset': {'in': 'query', 'description': 'id offset for pagination', 'default': '0'},
            'limit': {'in': 'query', 'description': 'number of entries to get', 'default': '50'},

        })
        @parking_ns.marshal_with(respList(parking_ns, ParkingSession))
        def get(self):
            """
            Only non-complete ParkingSessions with last_update between the given {date_from} (including) and {date_to} (excluding) will be returned.
            """
            parser = pagination_parser()
            args = parser.parse_args()
            return make_response(self.parking_manager.getParkingSessions,
                                 args["from"], args["to"], args["offset"], args["limit"]
                                 )

    @parking_ns.route(
        "/<string:country_id>/<string:party_id>/<string:reservation_id>",
        doc={"description": "API Endpoint for ParkingSession management"},
    )
    @parking_ns.response(404, "Command not found")
    @parking_ns.expect(header_parser)
    class start_parking(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.parking_manager = kwargs["parking"]
            super().__init__(api, *args, **kwargs)

        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=404)
        @token_required
        def get(self, country_id, party_id, session_id):

            return make_response(self.parking_manager.getParkingSession,
                                 country_id, party_id, session_id)

        @parking_ns.expect(ParkingSession, validate=False)
        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=201)
        @token_required
        def patch(self, country_id, party_id, reservation_id):
            '''
            Patch existing ParkingSession.
            ParkingSession can have status REQUEST for price requests.
            Pending Reservations will be turned to Sessions when scheduled
            '''
            reservation_id = reservation_id.upper()  # caseinsensitive
            country_id = country_id.upper()
            party_id = party_id.upper()

            return make_response(self.parking_manager.updateParkingSession,
                                 country_id, party_id, reservation_id, parking_ns.payload)


def receiver():
    @parking_ns.route(
        "/<string:country_id>/<string:party_id>/<string:session_id>",
        doc={"description": "API Endpoint for Session management"},
    )
    @parking_ns.response(404, "Command not found")
    @parking_ns.expect(header_parser)
    class receiver_session(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.parking_manager = kwargs["parking"]
            super().__init__(api, *args, **kwargs)

        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=200)
        @token_required
        def get(self, country_id, party_id, session_id):
            """Get current information for Parkingsession"""
            return make_response(self.parking_manager.getParkingSession,
                                 country_id, party_id, session_id)

        @parking_ns.expect(ParkingSession)
        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=201)
        @token_required
        def put(self, country_id, party_id, session_id):
            """Add new Parkingsession"""
            session_id = session_id.upper()  # caseinsensitive
            country_id = country_id.upper()
            party_id = party_id.upper()

            return make_response(self.parking_manager.createParkingSession,
                                 country_id, party_id, session_id,
                                 parking_ns.payload)

        @parking_ns.expect(ParkingSession, validate=False)
        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=201)
        @token_required
        def patch(self, country_id, party_id, session_id):
            """Update existing Parkingsession"""
            session_id = session_id.upper()  # caseinsensitive
            country_id = country_id.upper()
            party_id = party_id.upper()

            return make_response(self.parking_manager.patchParkingSession,
                                country_id,
                                party_id,
                                session_id,
                                parking_ns.payload)
            # TODO save and process preferences somewhere

    return parking_ns


def makeParkingNamespace(role):
    if role == 'SENDER':
        sender()
    elif role == 'RECEIVER':
        receiver()
    else:
        raise Exception('invalid role')
    return parking_ns