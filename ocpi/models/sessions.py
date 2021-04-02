#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 22:29:19 2021

@author: maurer
"""

from flask_restx import fields, Model


############### Session Models ###############

token_type = ["AD_HOC_USER", "APP_USER", "OTHER", "RFID"]

CdrToken = Model('CdrToken', {
    'uid': fields.String(max_length=36, required=True, description="Unique ID by which this Token can be identified."),
    'type': fields.String(enum=token_type, required=True, description="Type of the token"),
    'contract_id': fields.String(max_length=36, required=True, description='Uniquely identifies the EV driver contract token within the eMSP’s platform (and suboperator platforms). Recommended to follow the specification for eMA ID from "eMI3 standard version V1.0" '),
})

cdr_dimension_type = ["CURRENT",
                      "ENERGY",
                      "ENERGY_EXPORT",
                      "ENERGY_IMPORT",
                      "MAX_CURRENT",
                      "MIN_CURRENT",
                      "MAX_POWER",
                      "MIN_POWER",
                      "PARKING_TIME",
                      "POWER",
                      "RESERVATION_TIME",
                      "STATE_OF_CHARGE",
                      "TIME"]


CdrDimension = Model('CdrDimension', {
    'type': fields.String(enum=cdr_dimension_type, description='Type of CDR dimension.'),
    'volume':  fields.Float(description='Volume of the dimension consumed, measured according to the dimension type.'),
})


ChargingPeriod = Model('ChargingPeriod', {
    'start_date_time': fields.DateTime(description='Start timestamp of the charging period. A period ends when the next period starts. The last period ends when the session ends.'),
    'dimensions':  fields.Nested(CdrDimension, description='List of relevant values for this charging period.'),
    'tariff_id': fields.String(max_length=36, description='Unique identifier of the Tariff that is relevant for this Charging Period. If not provided, no Tariff is relevant during this period.'),
})


auth_method = ["AUTH_REQUEST", "COMMAND", "WHITELIST"]
session_status = ["ACTIVE", "COMPLETED", "INVALID", "PENDING", "RESERVATION"]

Session = Model('Session', {
    'country_id': fields.String(required=True, description="ISO-3166 alpha-2 country code of the CPO that 'owns' this Session."),
    'party_id': fields.String(required=True, description="CPO ID of the CPO that 'owns' this Session (following the ISO-15118 standard)."),
    'id': fields.String(max_length=36, required=True, description='The unique id that identifies the charging session in the CPO platform.'),
    'start_date_time': fields.DateTime(required=True, description='The timestamp when the session became ACTIVE in the Charge Point.'),
    'end_date_time': fields.DateTime(description='The timestamp when the session was completed/finished, charging might have finished before the session ends, for example: EV is full, but parking cost also has to be paid.', required=False),
    'kWh': fields.Float(default=0, description='How many kWh were charged.'),
    'cdr_token': fields.Nested(CdrToken, required=True, description='Token used to start this charging session, including all the relevant information to identify the unique token.'),
    'auth_method': fields.String(enum=auth_method, required=True, description='Method used for authentication.'),
    'authorization_reference': fields.String(max_length=36, description='Reference to the authorization given by the eMSP. When the eMSP provided an authorization_reference in either: real-time authorization or StartSession, this field SHALL contain the same value.', required=False),
    'location_id': fields.String(max_length=36, required=True, description='Location.id of the Location object of this CPO, on which the charging session is/was happening.'),
    'evse_uid': fields.String(max_length=36, required=True, description='EVSE.uid of the EVSE of this Location on which the charging session is/was happening.'),
    'connector_id': fields.String(max_length=36, required=True, description='Connector.id of the Connector of this Location the charging session is/was happening.'),
    'meter_id': fields.String(max_length=255, description='ISO 4217 code of the currency used for this session.', required=False),
    'currency': fields.String(max_length=3, required=True, description='Optional identification of the kWh meter.'),
    'charging_periods': fields.String(description='An optional list of Charging Periods that can be used to calculate and verify the total cost.', required=False),
    'total_cost': fields.Float(description='The total cost of the session in the specified currency. This is the price that the eMSP will have to pay to the CPO.'),
    'status': fields.String(enum=session_status, default="PENDING", description='The status of the session.'),
    'last_updated': fields.DateTime(description='Timestamp when this Session was last updated (or created).')
})

profile_type = ["CHEAP", "FAST", "GREEN", "REGULAR"]

ChargingPreferences = Model('ChargingPreferences', {
    'profile_type': fields.String(enum=profile_type, readonly=True, description='Type of Smart Charging Profile selected by the driver'),
    'departure_time': fields.String(required=True, description='Expected departure. The driver has given this Date/Time as expected departure moment. It is only an estimation and not necessarily the Date/Time of the actual departure.'),
    'energy_need': fields.Float(description='Requested amount of energy in kWh. The EV driver wants to have this amount of energy charged.'),
    'discharge_allowed': fields.Boolean(default=False, description='The driver allows their EV to be discharged when needed, as long as the other preferences are met'),
})


def add_models_to_session_namespace(namespace):
    for model in [CdrToken, CdrDimension, ChargingPeriod, Session, ChargingPreferences]:
        namespace.models[model.name] = model