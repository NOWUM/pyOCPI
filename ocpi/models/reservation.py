#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:05:59 2021

@author: maurer
"""
from flask_restx import Model, fields
from ocpi.models.sessions import auth_method, CdrToken, ChargingPeriod
reservation_status = ["REQUEST", "ACTIVE",
                      "COMPLETED", "INVALID", "PENDING", "RESERVATION"]
Reservation = Model('Reservation', {
    'country_id': fields.String(required=True, description="ISO-3166 alpha-2 country code of the CPO that 'owns' this Session."),
    'party_id': fields.String(required=True, description="CPO ID of the CPO that 'owns' this Session (following the ISO-15118 standard)."),
    'id': fields.String(max_length=36, required=True, description='The unique id that identifies the charging session in the CPO platform.'),
    'start_date_time': fields.DateTime(required=True, description='The timestamp when the session became ACTIVE in the Charge Point.'),
    'end_date_time': fields.DateTime(description='The timestamp when the session was completed/finished, charging might have finished before the session ends, for example: EV is full, but parking cost also has to be paid.', required=False),
    'energy_need': fields.Float(default=0, description='How many kWh are requested as maximum.'),
    'auth_method': fields.String(enum=auth_method, required=True, description='Method used for authentication.'),
    'location_id': fields.String(max_length=36, required=True, description='Location.id of the Location object of this CPO, on which the charging session is/was happening.'),
    'connector_type': fields.String(max_length=36, required=True, description='Connector.id of the Connector of this Location the charging session is/was happening.'),
    'currency': fields.String(max_length=3, description='ISO 4217 code of the currency used for this session.'),
    'total_cost': fields.Float(description='The total cost of the session in the specified currency. This is the price that the eMSP will have to pay to the CPO.'),
    'status': fields.String(enum=reservation_status, default="REQUEST", description='The status of the reservation.'),
    'last_updated': fields.DateTime(description='Timestamp when this Session was last updated (or created).'),
    'license_plate': fields.String(description='The optional license plate for recognition at a car park'),
})


def add_models_to_reservation_namespace(namespace):
    for model in [CdrToken, ChargingPeriod, Reservation]:
        namespace.models[model.name] = model