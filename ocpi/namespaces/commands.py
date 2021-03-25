#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:26:15 2021

@author: maurer
"""

from flask_restx import Resource, Namespace
from ocpi.models import StartSession, StopSession, UnlockConnector, CommandResponse, CommandResult, CancelReservation, ReserveNow

commands_ns = Namespace(name="commands", validate=True)
commands_ns.models[StartSession.name] = StartSession
commands_ns.models[StopSession.name] = StopSession
commands_ns.models[UnlockConnector.name] = UnlockConnector
commands_ns.models[CommandResponse.name] = CommandResponse
commands_ns.models[CommandResult.name] = CommandResult
commands_ns.models[CancelReservation.name] = CancelReservation
commands_ns.models[ReserveNow.name] = ReserveNow


@commands_ns.route('/START_SESSION', doc={"description": "OCPI Command API"},)
@commands_ns.response(404, 'Command not found')
class start_session(Resource):
    @commands_ns.doc('PostCommand')  # operationId
    @commands_ns.expect(StartSession)
    @commands_ns.marshal_with(StartSession, code=201)
    def post(self):
        '''Start Charging Session'''
        # return resMan.create(api.payload), 201
        pass


@commands_ns.route('/STOP_SESSION', doc={"description": "OCPI Command API"},)
@commands_ns.response(404, 'Command not found')
class stop_session(Resource):
    @commands_ns.expect(StopSession)
    @commands_ns.marshal_with(StopSession, code=201)
    @commands_ns.marshal_with(CommandResult, code=200)
    @commands_ns.marshal_with(CommandResponse, code=200)
    def post(self):
        '''Stop Charging Session'''
        # return resMan.create(api.payload), 201
        pass


@commands_ns.route('/UNLOCK_CONNECTOR', doc={"description": "OCPI Command API"},)
@commands_ns.response(404, 'Command not found')
class unlock_connector(Resource):
    @commands_ns.expect(UnlockConnector)
    @commands_ns.marshal_with(UnlockConnector, code=201)
    @commands_ns.marshal_with(CommandResponse, code=200)
    def post(self):
        '''Unlock Connector'''
        # return resMan.create(api.payload), 201
        pass


@commands_ns.route('/CANCEL_RESERVATION', doc={"description": "OCPI Command API"},)
@commands_ns.response(404, 'Command not found')
class cancel_reservation(Resource):
    @commands_ns.expect(UnlockConnector)
    @commands_ns.marshal_with(CancelReservation, code=201)
    @commands_ns.marshal_with(CommandResponse, code=200)
    def post(self):
        '''cancel reservation'''
        # return resMan.create(api.payload), 201
        pass


@commands_ns.route('/RESERVE_NOW', doc={"description": "OCPI Command API"},)
@commands_ns.response(404, 'Command not found')
class resrve_now(Resource):
    @commands_ns.expect(UnlockConnector)
    @commands_ns.marshal_with(ReserveNow, code=201)
    @commands_ns.marshal_with(CommandResponse, code=200)
    def post(self):
        '''resrve Now'''
        # return resMan.create(api.payload), 201
        pass
