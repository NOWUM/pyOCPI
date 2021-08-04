#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:26:15 2021

@author: maurer
"""

from datetime import datetime
from ocpi.decorators import token_required, get_header_parser, _check_access_token
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
        self.cm = kwargs['commands']
        super().__init__(api, *args, **kwargs)

    @commands_ns.doc('PostCommand')  # operationId
    @commands_ns.expect(parser, StartSession)
    @commands_ns.marshal_with(resp(commands_ns, CommandResponse), code=201)
    @token_required
    def post(self):
        '''Start Charging Session'''
        token = _check_access_token()
        data = self.cm.startSession(commands_ns.payload, token)
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }


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
        data = self.cm.stopSession(commands_ns.payload, token)
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }


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
        data = self.cm.unlockConnector(commands_ns.payload, token)
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }


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
        '''cancel reservation'''
        token = _check_access_token()
        data = self.cm.cancelReservation(commands_ns.payload, token)
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }


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
        '''reserve Now'''
        token = _check_access_token()
        data = self.cm.reserveNow(commands_ns.payload, token)
        return {'data': data,
                'status_code': 1000,
                'status_message': 'nothing',
                'timestamp': datetime.now()
                }