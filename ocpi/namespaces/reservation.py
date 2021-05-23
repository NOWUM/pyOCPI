#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:05:54 2021

@author: maurer

Custom sender module for reservation management

reservation can be a request query or a reservation, which gets transferred to a real session
"""


from flask_restx import Resource, Namespace
from flask_restx.inputs import datetime_from_iso8601
from ocpi.models.reservation import add_models_to_reservation_namespace, Reservation
from flask_restx import reqparse
from ocpi.models import resp, respList
from ocpi.decorators import get_header_parser
from datetime import datetime

reservation_ns = Namespace(name="reservations", validate=True)
add_models_to_reservation_namespace(reservation_ns)
header_parser = get_header_parser(reservation_ns)


def receiverNamespace():
    @reservation_ns.route('/<string:country_id>/<string:party_id>/<string:reservation_id>', doc={"description": "API Endpoint for Reservation management"})
    @reservation_ns.response(404, 'Command not found')
    @reservation_ns.expect(header_parser)
    class start_reservation(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.reservation_manager = kwargs['reservations']
            super().__init__(api, *args, **kwargs)

        @reservation_ns.marshal_with(resp(reservation_ns, Reservation), code=404)
        def get(self, country_id, party_id, reservation_id):

            try:
                ses = self.reservation_manager.getReservation(
                    country_id, party_id, reservation_id)
                # TODO validate country and party
            except:
                return '', 404

            return {'data': ses,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        @reservation_ns.expect(Reservation, validate=False)
        @reservation_ns.marshal_with(resp(reservation_ns, Reservation), code=201)
        def patch(self, country_id, party_id, reservation_id):
            '''
            Patch existing Reservation.
            Reservation can have status REQUEST for price requests.
            Pending Reservations will be turned to Sessions when scheduled
            '''
            reservation_id = reservation_id.lower()  # caseinsensitive
            country_id = country_id.lower()
            party_id = party_id.lower()

            data = self.reservation_manager.updateReservation(
                country_id, party_id, reservation_ns.payload)
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }


def senderNamespace():
    @reservation_ns.route('/', doc={"description": "API Endpoint for Reservation management"})
    @reservation_ns.expect(header_parser)
    class get_reservation(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.reservation_manager = kwargs['reservations']
            super().__init__(api, *args, **kwargs)

        @reservation_ns.doc(params={
            'from': {'in': 'query', 'description': 'declare Reservation start point', 'default': '2021-01-01T13:30:00+02:00', 'required': True},
            'to': {'in': 'query', 'description': 'declare Reservation end point', 'default': '2038-01-01T15:30:00+02:00', 'required': True},
            'offset': {'in': 'query', 'description': 'id offset for pagination', 'default': '0'},
            'limit': {'in': 'query', 'description': 'number of entries to get', 'default': '50'},

        })
        @reservation_ns.marshal_with(respList(reservation_ns, Reservation))
        def get(self):
            '''
            Only Reservations with last_update between the given {date_from} (including) and {date_to} (excluding) will be returned.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('from', type=datetime_from_iso8601)
            parser.add_argument('to', type=datetime_from_iso8601)
            parser.add_argument('offset', type=int)
            parser.add_argument('limit', type=int)
            args = parser.parse_args()
            data = self.reservation_manager.getReservations(
                args['from'], args['to'], args['offset'], args['limit'])
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

    @reservation_ns.route('/<string:country_id>/<string:party_id>/<string:reservation_id>', doc={"description": "API Endpoint for Reservation management"})
    @reservation_ns.response(404, 'Command not found')
    @reservation_ns.expect(header_parser)
    class start_reservation(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.reservation_manager = kwargs['reservations']
            super().__init__(api, *args, **kwargs)

        @reservation_ns.marshal_with(resp(reservation_ns, Reservation), code=404)
        def get(self, country_id, party_id, reservation_id):

            try:
                ses = self.reservation_manager.getReservation(
                    country_id, party_id, reservation_id)
                # TODO validate country and party
            except:
                return '', 404

            return {'data': ses,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        @reservation_ns.expect(Reservation)
        @reservation_ns.marshal_with(resp(reservation_ns, Reservation), code=201)
        def post(self, country_id, party_id, reservation_id):
            '''
            Add new Reservation.
            Reservation can have status REQUEST for price requests.
            Pending Reservations will be turned to Sessions when scheduled
            '''
            reservation_id = reservation_id.lower()  # caseinsensitive
            country_id = country_id.lower()
            party_id = party_id.lower()

            data = self.reservation_manager.addReservation(
                country_id, party_id, reservation_ns.payload)
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        @reservation_ns.expect(Reservation, validate=False)
        @reservation_ns.marshal_with(resp(reservation_ns, Reservation), code=201)
        def patch(self, country_id, party_id, reservation_id):
            '''
            Patch existing Reservation.
            Reservation can have status REQUEST for price requests.
            Pending Reservations will be turned to Sessions when scheduled
            '''
            reservation_id = reservation_id.lower()  # caseinsensitive
            country_id = country_id.lower()
            party_id = party_id.lower()

            data = self.reservation_manager.updateReservation(
                country_id, party_id, reservation_ns.payload)
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }


def makeReservationNamespace(interfaces=["SENDER", "RECEIVER"]):
    if "SENDER" in interfaces:
        senderNamespace()
    if "RECEIVER" in interfaces:
        receiverNamespace()
    return reservation_ns