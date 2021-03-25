#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:21:29 2021

@author: maurer
"""

from flask_restx import fields, Model

CancelReservation = Model('CancelReservation', {
    'response_url': fields.String(readonly=True, description='URL that the CommandResult POST should be sent to. This URL might contain an unique ID to be able to distinguish between StopSession requests.'),
    'reservation_id': fields.String(required=True, description='Reservation id, unique for this reservation. If the Receiver (typically CPO) Point already has a reservation that matches this reservationId for that Location it will replace the reservation.'),
})

ReserveNow = Model('ReserveNow', {
    'response_url': fields.String(required=True, description='URL that the CommandResult POST should be sent to. This URL might contain an unique ID to be able to distinguish between StartSession requests.'),
    'token': fields.String(required=True, description='Token object the Charge Point has to use to start a new session. The Token provided in this request is authorized by the eMSP.'),
    'expiry_date': fields.DateTime(description='Timestamp when this Session was last updated (or created).'),
    'reservation_id': fields.String(required=True, description='Reservation id, unique for this reservation. If the Receiver (typically CPO) Point already has a reservation that matches this reservationId for that Location it will replace the reservation.'),
    'location_id': fields.String(required=True, description='Location.id of the Location (belonging to the CPO this request is send to) on which a session is to be started.'),
    'evse_uid': fields.String(description='Optional EVSE.uid of the EVSE of this Location on which a session is to be started.'),
    'authorization_reference': fields.String(description='Reference to the authorization given by the eMSP, when given, this reference will be provided in the relevant Session and/or CDR.')
})

StartSession = Model('StartSession', {
    'response_url': fields.String(required=True, description='URL that the CommandResult POST should be sent to. This URL might contain an unique ID to be able to distinguish between StartSession requests.'),
    'token': fields.String(required=True, description='Token object the Charge Point has to use to start a new session. The Token provided in this request is authorized by the eMSP.'),
    'location_id': fields.String(required=True, description='Location.id of the Location (belonging to the CPO this request is send to) on which a session is to be started.'),
    'evse_uid': fields.String(description='Optional EVSE.uid of the EVSE of this Location on which a session is to be started.'),
    'authorization_reference': fields.String(description='Reference to the authorization given by the eMSP, when given, this reference will be provided in the relevant Session and/or CDR.')
})

StopSession = Model('StopSession', {
    'response_url': fields.String(readonly=True, description='URL that the CommandResult POST should be sent to. This URL might contain an unique ID to be able to distinguish between StopSession requests.'),
    'session_id': fields.String(required=True, description='Session.id of the Session that is requested to be stopped.'),
})

UnlockConnector = Model('UnlockConnector', {
    'response_url': fields.String(readonly=True, description='URL that the CommandResult POST should be sent to. This URL might contain an unique ID to be able to distinguish between UnlockConnector requests.'),
    'location_id': fields.String(required=True, description='Location.id of the Location (belonging to the CPO this request is send to) of which it is requested to unlock the connector.'),
    'evse_uid': fields.String(description='EVSE.uid of the EVSE of this Location of which it is requested to unlock the connector.'),
    'connector_id': fields.String(default=True, description='Connector.id of the Connector of this Location of which it is requested to unlock.')
})

command_response = ['NOT_SUPPORTED', 'REJECTED', 'ACCEPTED', 'UNKNOWN_SESSION']
CommandResponse = Model('CommandResponse', {
    'result': fields.String(enum=command_response, readonly=True, description='Response from the CPO on the command request.'),
    'timeout': fields.Integer(description='Timeout for this command in seconds. When the Result is not received within this timeout, the eMSP can assume that the message might never be send.'),
    'message': fields.String(required=True, description='Human-readable description of the result (if one can be provided), multiple languages can be provided.'),
})

command_result = ['ACCEPTED', 'CANCELED_RESERVATION', 'EVSE_OCCUPIED', 'EVSE_INOPERATIVE',
                  'FAILED', 'NOT_SUPPORTED', 'REJECTED', 'TIMEOUT', 'UNKNOWN_RESERVATION']
CommandResult = Model('CommandResult', {
    'result': fields.String(enum=command_result, readonly=True, description='Result of the command request as sent by the Charge Point to the CPO.'),
    'message': fields.String(required=True, description='Human-readable description of the result (if one can be provided), multiple languages can be provided.'),
})


profile_type = ["CHEAP", "FAST", "GREEN", "REGULAR"]

ChargingPreferences = Model('ChargingPreferences', {
    'profile_type': fields.String(enum=profile_type, readonly=True, description='Type of Smart Charging Profile selected by the driver'),
    'departure_time': fields.String(required=True, description='Expected departure. The driver has given this Date/Time as expected departure moment. It is only an estimation and not necessarily the Date/Time of the actual departure.'),
    'energy_need': fields.Float(description='Requested amount of energy in kWh. The EV driver wants to have this amount of energy charged.'),
    'discharge_allowed': fields.Boolean(default=False, description='The driver allows their EV to be discharged when needed, as long as the other preferences are met'),
})


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


def add_models_to_session_namespace(namespace):
    for model in [CdrToken, CdrDimension, ChargingPeriod, Session, ChargingPreferences]:
        namespace.models[model.name] = model
