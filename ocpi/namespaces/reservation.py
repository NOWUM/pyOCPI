#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:05:54 2021

@author: maurer

Custom sender module for reservation management

reservation can be a request query or a reservation, which gets transferred to a real session
"""


from flask_restx import Resource, Namespace
from ocpi.models import resp, respList
from ocpi.models.reservation import add_models_to_reservation_namespace, Reservation
from ocpi.namespaces import (get_header_parser, token_required,
                             pagination_parser, make_response)

reservation_ns = Namespace(name="reservations", validate=True)
add_models_to_reservation_namespace(reservation_ns)
header_parser = get_header_parser(reservation_ns)


def receiver():
    @reservation_ns.route('/<string:country_id>/<string:party_id>/<string:reservation_id>', doc={"description": "API Endpoint for Reservation management"})
    @reservation_ns.response(404, 'Command not found')
    @reservation_ns.expect(header_parser)
    class update_reservations(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.reservation_manager = kwargs['reservations']
            super().__init__(api, *args, **kwargs)

        @reservation_ns.marshal_with(resp(reservation_ns, Reservation), code=404)
        @token_required
        def get(self, country_id, party_id, reservation_id):
            '''
            Get the current reservation from the eMSP.
            '''
            return make_response(self.reservation_manager.getReservation,
                                 country_id, party_id, reservation_id)

        @reservation_ns.expect(Reservation)
        @reservation_ns.marshal_with(respList(reservation_ns, Reservation), code=201)
        @token_required
        def put(self, country_id, party_id, reservation_id):
            '''
            Update the reservation of the CPO at the eMSP to announce a changed state.
            '''
            reservation_id = reservation_id.upper()  # caseinsensitive
            country_id = country_id.upper()
            party_id = party_id.upper()

            return make_response(self.reservation_manager.addReservation,
                                 country_id, party_id, reservation_ns.payload)

        @reservation_ns.expect(Reservation, validate=False)
        @reservation_ns.marshal_with(resp(reservation_ns, Reservation), code=201)
        @token_required
        def patch(self, country_id, party_id, reservation_id):
            '''
            Patch existing Reservation.
            Reservation can have status REQUEST for price requests.
            Pending Reservations will be turned to Sessions when scheduled
            '''
            reservation_id = reservation_id.upper()  # caseinsensitive
            country_id = country_id.upper()
            party_id = party_id.upper()

            return make_response(self.reservation_manager.updateReservation,
                                 country_id, party_id, reservation_ns.payload)


def sender():
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
        @token_required
        def get(self):
            '''
            Get Reservations from the CPO where the eMSP is responsible for.
            Only Reservations with last_update between the given {date_from} (including) and {date_to} (excluding) will be returned.
            '''
            parser = pagination_parser()
            args = parser.parse_args()
            return make_response(self.reservation_manager.getReservations,
                                 args['from'], args['to'], args['offset'], args['limit'])

    @reservation_ns.route('/<string:country_id>/<string:party_id>/<string:reservation_id>', doc={"description": "API Endpoint for Reservation management"})
    @reservation_ns.response(404, 'Command not found')
    @reservation_ns.expect(header_parser)
    class add_reservations(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.reservation_manager = kwargs['reservations']
            super().__init__(api, *args, **kwargs)

        @reservation_ns.marshal_with(resp(reservation_ns, Reservation), code=404)
        @token_required
        def get(self, country_id, party_id, reservation_id):

            return make_response(self.reservation_manager.getReservation,
                                 country_id, party_id, reservation_id)

        @reservation_ns.expect(Reservation)
        @reservation_ns.marshal_with(respList(reservation_ns, Reservation), code=201)
        @token_required
        def post(self, country_id, party_id, reservation_id):
            '''
            Request new Reservation at the CPO.
            Reservation can have status REQUEST for price requests.
            Pending Reservations will be turned to Sessions when scheduled
            '''
            reservation_id = reservation_id.upper()  # caseinsensitive
            country_id = country_id.upper()
            party_id = party_id.upper()

            return make_response(self.reservation_manager.addReservation,
                                 country_id, party_id, reservation_ns.payload)

        @reservation_ns.expect(Reservation, validate=False)
        @reservation_ns.marshal_with(resp(reservation_ns, Reservation), code=201)
        @token_required
        def patch(self, country_id, party_id, reservation_id):
            '''
            Patch existing Reservation at the CPO.
            Reservation can have status REQUEST for price requests.
            Pending Reservations will be turned to Sessions when scheduled
            '''
            reservation_id = reservation_id.upper()  # caseinsensitive
            # TODO validate reservation_id with payload
            country_id = country_id.upper()
            party_id = party_id.upper()

            return make_response(self.reservation_manager.updateReservation,
                                 country_id, party_id, reservation_ns.payload)


def makeReservationNamespace(role):
    if role == 'SENDER':
        sender()
    elif role == 'RECEIVER':
        receiver()
    else:
        raise Exception('invalid role')
    return reservation_ns
