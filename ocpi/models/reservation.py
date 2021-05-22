#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:05:59 2021

@author: maurer
"""
from .sessions import BaseSession
from flask_restx import fields
from ocpi.models.sessions import auth_method, CdrToken, ChargingPeriod
reservation_status = ["REQUEST", "ACTIVE",
                      "COMPLETED", "INVALID", "PENDING", "RESERVATION"]

Reservation = BaseSession.clone('Reservation', {
    'energy_need': fields.Float(default=0, description='How many kWh are requested as maximum.'),
    'auth_method': fields.String(enum=auth_method, required=True, description='Method used for authentication.'),
    'connector_type': fields.String(max_length=36, required=True, description='Connector.id of the Connector of this Location the charging session is/was happening.'),
    'currency': fields.String(max_length=3, description='ISO 4217 code of the currency used for this session.'),
    'total_cost': fields.Float(description='The total cost of the session in the specified currency. This is the price that the eMSP will have to pay to the CPO.'),
    'status': fields.String(enum=reservation_status, default="REQUEST", description='The status of the reservation.'),
    'license_plate': fields.String(description='The optional license plate for recognition at a car park'),
})


def add_models_to_reservation_namespace(namespace):
    for model in [CdrToken, ChargingPeriod, Reservation]:
        namespace.models[model.name] = model