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
from flask_restx.inputs import datetime_from_iso8601
from ocpi.models.parking import add_models_to_parking_namespace, ParkingSession
from flask_restx import reqparse
from ocpi.models import resp, respList
from ocpi.decorators import get_header_parser
from datetime import datetime

parking_ns = Namespace(name="parking", validate=True)
add_models_to_parking_namespace(parking_ns)
header_parser = get_header_parser(parking_ns)


def senderNamespace():
    @parking_ns.route('/', doc={"description": "API Endpoint for ParkingSession management"})
    @parking_ns.expect(header_parser)
    class get_parking_sessions(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.parking_manager = kwargs['parking']
            super().__init__(api, *args, **kwargs)

        @parking_ns.doc(params={
            'from': {'in': 'query', 'description': 'declare ParkingSession start point', 'default': '2021-01-01T13:30:00+02:00', 'required': True},
            'to': {'in': 'query', 'description': 'declare ParkingSession end point', 'default': '2038-01-01T15:30:00+02:00', 'required': True},
            'offset': {'in': 'query', 'description': 'id offset for pagination', 'default': '0'},
            'limit': {'in': 'query', 'description': 'number of entries to get', 'default': '50'},

        })
        @parking_ns.marshal_with(respList(parking_ns, ParkingSession))
        def get(self):
            '''
            Only ParkingSessions with last_update between the given {date_from} (including) and {date_to} (excluding) will be returned.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('from', type=datetime_from_iso8601)
            parser.add_argument('to', type=datetime_from_iso8601)
            parser.add_argument('offset', type=int)
            parser.add_argument('limit', type=int)
            args = parser.parse_args()
            data = self.parking_manager.getParkingSessions(
                args['from'], args['to'], args['offset'], args['limit'])
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }


    @parking_ns.route('/<string:country_id>/<string:party_id>/<string:reservation_id>', doc={"description": "API Endpoint for ParkingSession management"})
    @parking_ns.response(404, 'Command not found')
    @parking_ns.expect(header_parser)
    class start_reservation(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.reservation_manager = kwargs['reservations']
            super().__init__(api, *args, **kwargs)

        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=404)
        def get(self, country_id, party_id, reservation_id):

            try:
                ses = self.parking_manager.getParkingSession(
                    country_id, party_id, reservation_id)
                # TODO validate country and party
            except:
                return '', 404

            return {'data': ses,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        @parking_ns.expect(ParkingSession)
        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=201)
        def put(self, country_id, party_id, reservation_id):
            '''
            Add new ParkingSession.
            ParkingSession can have status REQUEST for price requests.
            '''
            reservation_id = reservation_id.lower()  # caseinsensitive
            country_id = country_id.lower()
            party_id = party_id.lower()

            data = self.parking_manager.createParkingSession(
                country_id, party_id, parking_ns.payload)
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        @parking_ns.expect(ParkingSession, validate=False)
        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=201)
        def patch(self, country_id, party_id, reservation_id):
            '''
            Patch existing ParkingSession.
            ParkingSession can have status REQUEST for price requests.
            Pending Reservations will be turned to Sessions when scheduled
            '''
            reservation_id = reservation_id.lower()  # caseinsensitive
            country_id = country_id.lower()
            party_id = party_id.lower()

            data = self.parking_manager.updateParkingSession(
                country_id, party_id, parking_ns.payload)
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }



def receiverNamespace():
    @parking_ns.route('/<string:country_id>/<string:party_id>/<string:session_id>', doc={"description": "API Endpoint for Session management"})
    @parking_ns.response(404, 'Command not found')
    @parking_ns.expect(header_parser)
    class receiver_session(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.session_manager = kwargs['sessions']
            super().__init__(api, *args, **kwargs)

        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=200)
        def get(self, country_id, party_id, session_id):

            # TODO validate country and party
            return self.parking_manager.getParkingSession(session_id)

        @parking_ns.expect(ParkingSession)
        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=201)
        def put(self, country_id, party_id, session_id):
            '''Add new Session'''
            session_id = session_id.lower()  # caseinsensitive
            country_id = country_id.lower()
            party_id = party_id.lower()

            return self.parking_manager.createParkingSession(parking_ns.payload)

        @parking_ns.expect(ParkingSession, validate=False)
        @parking_ns.marshal_with(resp(parking_ns, ParkingSession), code=201)
        def patch(self, country_id, party_id, session_id):
            session_id = session_id.lower()  # caseinsensitive
            country_id = country_id.lower()
            party_id = party_id.lower()

            return self.parking_manager.patchParkingSession(session_id, parking_ns.payload)
            # TODO save and process preferences somewhere
    return parking_ns


def makeParkingNamespace(interfaces=['SENDER', 'RECEIVER']):
    if 'SENDER' in interfaces:
        senderNamespace()
    if 'RECEIVER' in interfaces:
        receiverNamespace()
    return parking_ns