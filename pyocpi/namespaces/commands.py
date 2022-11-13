#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: maurer
"""

import logging
from flask_restx import Resource, Namespace
from ocpi.models import resp
from ocpi.models.commands import (add_models_to_commands_namespace,
                                  StartSession, StopSession, UnlockConnector,
                                  CommandResponse, CommandResult,
                                  CancelReservation, ReserveNow)
from ocpi.namespaces import (token_required, get_header_parser,
                             _check_access_token, make_response)

commands_ns = Namespace(name="commands", validate=True)
add_models_to_commands_namespace(commands_ns)

parser = get_header_parser(commands_ns)

log = logging.getLogger('ocpi')


def sender():
    @commands_ns.route('/START_SESSION', doc={"description": "OCPI Command API"},)
    @commands_ns.response(404, 'Command not found')
    class start_session(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.cm = kwargs['commands']
            super().__init__(api, *args, **kwargs)

        @commands_ns.doc('PostCommand')  # operationId
        @commands_ns.expect(parser, StartSession)
        @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=201)
        @token_required
        def post(self):
            '''Start Charging Session'''
            token = _check_access_token()
            return make_response(self.cm.startSession, commands_ns.payload, token)

    @commands_ns.route('/STOP_SESSION', doc={"description": "OCPI Command API"},)
    @commands_ns.response(404, 'Command not found')
    class stop_session(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.cm = kwargs['commands']
            super().__init__(api, *args, **kwargs)

        @commands_ns.expect(parser, StopSession)
        @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=200)
        @token_required
        def post(self):
            '''Stop Charging Session'''
            token = _check_access_token()
            return make_response(self.cm.stopSession, commands_ns.payload, token)

    @commands_ns.route('/UNLOCK_CONNECTOR', doc={"description": "OCPI Command API"},)
    @commands_ns.response(404, 'Command not found')
    class unlock_connector(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.cm = kwargs['commands']
            super().__init__(api, *args, **kwargs)

        @commands_ns.expect(parser, UnlockConnector)
        @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=200)
        @token_required
        def post(self):
            '''Unlock Connector'''
            token = _check_access_token()
            return make_response(self.cm.unlockConnector, commands_ns.payload, token)

    @commands_ns.route('/CANCEL_RESERVATION', doc={"description": "OCPI Command API"},)
    @commands_ns.response(404, 'Command not found')
    class cancel_reservation(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.cm = kwargs['commands']
            super().__init__(api, *args, **kwargs)

        @commands_ns.expect(parser, CancelReservation)
        @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=200)
        @token_required
        def post(self):
            '''Cancel Reservation'''
            token = _check_access_token()
            return make_response(self.cm.cancelReservation, commands_ns.payload, token)

    @commands_ns.route('/RESERVE_NOW', doc={"description": "OCPI Command API"},)
    @commands_ns.response(404, 'Command not found')
    class reserve_now(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.cm = kwargs['commands']
            super().__init__(api, *args, **kwargs)

        @commands_ns.expect(parser, ReserveNow)
        @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=200)
        @token_required
        def post(self):
            '''Reserve Now'''
            token = _check_access_token()
            return make_response(self.cm.reserveNow, commands_ns.payload, token)


def receiver():
    @commands_ns.route('/START_SESSION_RESULT', doc={"description": "OCPI Command API"},)
    @commands_ns.response(404, 'Command not found')
    class start_session_result(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.cm = kwargs['commands']
            super().__init__(api, *args, **kwargs)

        @commands_ns.doc('PostCommandResult')  # operationId
        @commands_ns.expect(parser, CommandResult)
        @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=204)
        @token_required
        def post(self):
            '''Start Charging Session Answer'''
            token = _check_access_token()
            return make_response(self.cm.startSessionResult, commands_ns.payload, token)

    @commands_ns.route('/STOP_SESSION_RESULT', doc={"description": "OCPI Command API"},)
    @commands_ns.response(404, 'Command not found')
    class stop_session_result(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.cm = kwargs['commands']
            super().__init__(api, *args, **kwargs)

        @commands_ns.expect(parser, CommandResult)
        @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=204)
        @token_required
        def post(self):
            '''Stop Charging Session Answer'''
            token = _check_access_token()
            return make_response(self.cm.stopSessionResult, commands_ns.payload, token)

    @commands_ns.route('/UNLOCK_CONNECTOR_RESULT', doc={"description": "OCPI Command API"},)
    @commands_ns.response(404, 'Command not found')
    class unlock_connector_result(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.cm = kwargs['commands']
            super().__init__(api, *args, **kwargs)

        @commands_ns.expect(parser, CommandResult)
        @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=204)
        @token_required
        def post(self):
            '''Unlock Connector Answer'''
            return make_response(self.command_manager.unlockConnectorResult,
                                 commands_ns.payload)

    @commands_ns.route('/CANCEL_RESERVATION_RESULT', doc={"description": "OCPI Command API"},)
    @commands_ns.response(404, 'Command not found')
    class cancel_reservation_result(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.cm = kwargs['commands']
            super().__init__(api, *args, **kwargs)

        @commands_ns.expect(parser, CommandResult)
        @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=204)
        @token_required
        def post(self):
            '''Cancel Reservation Answer'''
            token = _check_access_token()
            return make_response(self.cm.cancelReservationResult, commands_ns.payload, token)

    @commands_ns.route('/RESERVE_NOW_RESULT', doc={"description": "OCPI Command API"},)
    @commands_ns.response(404, 'Command not found')
    class reserve_now_result(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.cm = kwargs['commands']
            super().__init__(api, *args, **kwargs)

        @commands_ns.expect(parser, CommandResult)
        @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=204)
        @token_required
        def post(self):
            '''Reserve Now Answer'''
            token = _check_access_token()
            return make_response(self.cm.reserveNowResult, commands_ns.payload, token)


def makeCommandsNamespace(role):
    if role == 'SENDER':
        sender()
    elif role == 'RECEIVER':
        receiver()
    else:
        raise Exception('invalid role')

    return commands_ns