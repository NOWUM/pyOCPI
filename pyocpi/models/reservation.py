#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:05:59 2021

@author: maurer
"""
from flask_restx import fields, Model
from .sessions import BaseSession, add_models_to_session_namespace
from .sessions import auth_method, CdrToken, ChargingPeriod, ChargingPreferences
from .location import connector_type, EnergyMix
from .tariffs import PriceComponent
from .types import CaseInsensitiveString

reservation_status = ["REQUEST", "ACTIVE",
                      "COMPLETED", "INVALID", "PENDING", "RESERVATION"]

ConnectorType = Model('ConnectorType', {
    'connector_type': fields.String(enum=connector_type, max_length=36, required=True, description='Connector.id of an available Connector'),
    'max_charging_speed': fields.Float(description='Maximum charging speed supported for this connector if lower than technical capabilities'),
})

Reservation = BaseSession.clone('Reservation', {
    'token_uid': fields.String(required=True, description='The uid of the Token for which this reservation was requested.'),
    'charging_preferences': fields.Nested(ChargingPreferences, required=True, description='Charging Preferences for OCPI'),
    'auth_method': fields.String(enum=auth_method, required=True, description='Method used for authentication.'),
    'connector_types': fields.List(fields.Nested(ConnectorType, description='Supported ConnectorTypes for the reservation')),
    'status': fields.String(enum=reservation_status, default="REQUEST", description='The status of the reservation.'),
    'license_plate': fields.String(description='The optional license plate for recognition at a car park'),
    'price_components': fields.List(fields.Nested(PriceComponent), description="List of Price Components needed to calculate the charging price"),
    'energy_mix': fields.Nested(EnergyMix, description='Name of the energy supplier, delivering the energy for this location or reservation'),
    'connect_date_time' : fields.DateTime(required=False, description='The timestamp when the session was connected to the CS. Can be omitted if same as start_date_time'),
    'disconnect_date_time' : fields.DateTime(required=False, description='The timestamp when the session was disconnected from the CS. Can be omitted if same as end_date_time'),
    'evse_uid': CaseInsensitiveString(max_length=36, description='EVSE.uid of the EVSE of this Location on which the charging session is/was happening.'),
    'connector_id': CaseInsensitiveString(max_length=36, description='Connector.id of the Connector of this Location the charging session is/was happening.'),
    'meter_id': fields.String(max_length=255, description='Optional identification of the kWh meter.'),
})


def add_models_to_reservation_namespace(namespace):
    for model in [CdrToken, ChargingPeriod, ConnectorType, Reservation, PriceComponent]:
        namespace.models[model.name] = model
    add_models_to_session_namespace(namespace)