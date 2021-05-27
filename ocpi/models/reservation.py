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
    'charging_preferences': fields.Nested(ChargingPreferences, required=True, description='Charging Preferences for OCPI'),
    'auth_method': fields.String(enum=auth_method, required=True, description='Method used for authentication.'),
    'connector_type': fields.String(enum=connector_type, max_length=36, required=True, description='Connector.id of the Connector of this Location the charging session is/was happening.'),
    'status': fields.String(enum=reservation_status, default="REQUEST", description='The status of the reservation.'),
    'license_plate': fields.String(description='The optional license plate for recognition at a car park'),
    'tariff_elements': fields.List(fields.Nested(TariffElement), description="List of Tariff elements needed to calculate the parking price"),
    'energy_mix': fields.Nested(EnergyMix, description='Name of the energy supplier, delivering the energy for this location or reservation'),
})


def add_models_to_reservation_namespace(namespace):
    for model in [CdrToken, ChargingPeriod, Reservation, TariffElement, TariffRestrictions, PriceComponent]:
        namespace.models[model.name] = model
    add_models_to_session_namespace(namespace)