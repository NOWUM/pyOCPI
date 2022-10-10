#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:21:29 2021

@author: maurer
"""
from flask_restx import fields, Model
from ocpi.models.types import DisplayText, CaseInsensitiveString
from ocpi.models.tokens import Token
############### Command Models ###############


CancelReservation = Model('CancelReservation', {
    'response_url': fields.String(required=True, description='URL that the CommandResult POST should be sent to. This URL might contain an unique ID to be able to distinguish between StopSession requests.'),
    'reservation_id': CaseInsensitiveString(required=True, description='Reservation id, unique for this reservation. If the Receiver (typically CPO) Point already has a reservation that matches this reservationId for that Location it will replace the reservation.'),
})

ReserveNow = Model('ReserveNow', {
    'response_url': fields.String(required=True, description='URL that the CommandResult POST should be sent to. This URL might contain an unique ID to be able to distinguish between StartSession requests.'),
    'token': fields.Nested(Token, required=True, description='Token object the Charge Point has to use to start a new session. The Token provided in this request is authorized by the eMSP.'),
    'expiry_date': fields.DateTime(description='Timestamp when this Session was last updated (or created).'),
    'reservation_id': CaseInsensitiveString(required=True, description='Reservation id, unique for this reservation. If the Receiver (typically CPO) Point already has a reservation that matches this reservationId for that Location it will replace the reservation.'),
    'location_id': CaseInsensitiveString(required=True, description='Location.id of the Location (belonging to the CPO this request is send to) on which a session is to be started.'),
    'evse_uid': CaseInsensitiveString(description='Optional EVSE.uid of the EVSE of this Location on which a session is to be started.'),
    'authorization_reference': CaseInsensitiveString(description='Reference to the authorization given by the eMSP, when given, this reference will be provided in the relevant Session and/or CDR.')
})

StartSession = Model('StartSession', {
    'response_url': fields.String(required=True, description='URL that the CommandResult POST should be sent to. This URL might contain an unique ID to be able to distinguish between StartSession requests.'),
    'token': fields.Nested(Token, required=True, description='Token object the Charge Point has to use to start a new session. The Token provided in this request is authorized by the eMSP.'),
    'location_id': CaseInsensitiveString(required=True, description='Location.id of the Location (belonging to the CPO this request is send to) on which a session is to be started.'),
    'evse_uid': CaseInsensitiveString(description='Optional EVSE.uid of the EVSE of this Location on which a session is to be started.'),
    'authorization_reference': CaseInsensitiveString(description='Reference to the authorization given by the eMSP, when given, this reference will be provided in the relevant Session and/or CDR.')
})

StopSession = Model('StopSession', {
    'response_url': fields.String(required=True, description='URL that the CommandResult POST should be sent to. This URL might contain an unique ID to be able to distinguish between StopSession requests.'),
    'session_id': fields.String(required=True, description='Session.id of the Session that is requested to be stopped.'),
})

UnlockConnector = Model('UnlockConnector', {
    'response_url': fields.String(required=True, description='URL that the CommandResult POST should be sent to. This URL might contain an unique ID to be able to distinguish between UnlockConnector requests.'),
    'location_id': CaseInsensitiveString(required=True, description='Location.id of the Location (belonging to the CPO this request is send to) of which it is requested to unlock the connector.'),
    'evse_uid': CaseInsensitiveString(description='EVSE.uid of the EVSE of this Location of which it is requested to unlock the connector.'),
    'connector_id': CaseInsensitiveString(default=True, description='Connector.id of the Connector of this Location of which it is requested to unlock.')
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
    'message': fields.List(fields.Nested(DisplayText), required=True, description='Human-readable description of the result (if one can be provided), multiple languages can be provided.'),
})


def add_models_to_commands_namespace(namespace):
    for model in [CommandResult, CommandResponse, UnlockConnector, StopSession, StartSession, ReserveNow, CancelReservation]:
        namespace.models[model.name] = model