#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:26:15 2021

@author: maurer
"""

from ocpi.decorators import token_required, get_header_parser
from flask_restx import Resource, Namespace
from ocpi.models.commands import (add_models_to_commands_namespace,
                                  StartSession, StopSession, UnlockConnector,
                                  CommandResponse, CancelReservation, ReserveNow)
from ocpi.models import resp
commands_ns = Namespace(name="commands", validate=True)
add_models_to_commands_namespace(commands_ns)


parser = get_header_parser(commands_ns)


@commands_ns.route('/START_SESSION', doc={"description": "OCPI Command API"},)
@commands_ns.response(404, 'Command not found')
class start_session(Resource):

    def __init__(self, api=None, *args, **kwargs):
        self.command_manager = kwargs['commands']
        super().__init__(api, *args, **kwargs)

    @commands_ns.doc('PostCommand')  # operationId
    @commands_ns.expect(parser, StartSession)
    @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=201)
    @token_required
    def post(self):
        '''Start Charging Session'''
        return self.command_manager.startSession(commands_ns.payload)


@commands_ns.route('/STOP_SESSION', doc={"description": "OCPI Command API"},)
@commands_ns.response(404, 'Command not found')
class stop_session(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.command_manager = kwargs['commands']
        super().__init__(api, *args, **kwargs)

    @commands_ns.expect(parser, StopSession)
    @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=200)
    @token_required
    def post(self):
        '''Stop Charging Session'''
        return self.command_manager.stopSession(commands_ns.payload)


@commands_ns.route('/UNLOCK_CONNECTOR', doc={"description": "OCPI Command API"},)
@commands_ns.response(404, 'Command not found')
class unlock_connector(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.command_manager = kwargs['commands']
        super().__init__(api, *args, **kwargs)

    @commands_ns.expect(parser, UnlockConnector)
    @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=200)
    @token_required
    def post(self):
        '''Unlock Connector'''
        return self.command_manager.unlockConnector(commands_ns.payload)


@commands_ns.route('/CANCEL_RESERVATION', doc={"description": "OCPI Command API"},)
@commands_ns.response(404, 'Command not found')
class cancel_reservation(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.command_manager = kwargs['commands']
        super().__init__(api, *args, **kwargs)

    @commands_ns.expect(parser, CancelReservation)
    @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=200)
    @token_required
    def post(self):
        '''cancel reservation'''
        return self.command_manager.cancelReservation(commands_ns.payload)


@commands_ns.route('/RESERVE_NOW', doc={"description": "OCPI Command API"},)
@commands_ns.response(404, 'Command not found')
class reserve_now(Resource):
    def __init__(self, api=None, *args, **kwargs):
        self.command_manager = kwargs['commands']
        super().__init__(api, *args, **kwargs)

    @commands_ns.expect(parser, ReserveNow)
    @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=200)
    @token_required
    def post(self):
        '''resrve Now'''
        return self.command_manager.reserveNow(commands_ns.payload)