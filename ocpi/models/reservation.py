#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:05:59 2021

@author: maurer
"""
from flask_restx import fields
from .sessions import BaseSession, add_models_to_session_namespace
from .sessions import auth_method, CdrToken, ChargingPeriod, ChargingPreferences
from .location import connector_type, EnergyMix
from .tariffs import TariffElement, TariffRestrictions, PriceComponent

reservation_status = ["REQUEST", "ACTIVE",
                      "COMPLETED", "INVALID", "PENDING", "RESERVATION"]

Reservation = BaseSession.clone('Reservation', {
    'token_uid': fields.String(required=True, description='The uid of the Token for which this reservation was requested.'),
    'charging_preferences': fields.Nested(ChargingPreferences, required=True, description='Charging Preferences for OCPI'),
    'auth_method': fields.String(enum=auth_method, required=True, description='Method used for authentication.'),
    'connector_type': fields.String(enum=connector_type, max_length=36, required=True, description='Connector.id of the Connector of this Location the charging session is/was happening.'),
    'status': fields.String(enum=reservation_status, default="REQUEST", description='The status of the reservation.'),
    'license_plate': fields.String(description='The optional license plate for recognition at a car park'),
    'price_components': fields.List(fields.Nested(PriceComponent), description="List of Price Components needed to calculate the charging price"),
    'energy_mix': fields.Nested(EnergyMix, description='Name of the energy supplier, delivering the energy for this location or reservation'),
    'max_charging_speed': fields.Float(description='Maximum charging speed if lower than selected connectors capabilities'),
})


def add_models_to_reservation_namespace(namespace):
    for model in [CdrToken, ChargingPeriod, Reservation, TariffElement, TariffRestrictions, PriceComponent]:
        namespace.models[model.name] = model
    add_models_to_session_namespace(namespace)