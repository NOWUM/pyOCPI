#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:26:34 2021

@author: maurer
"""
from flask_restx import Resource, Namespace
from ocpi.models.commands import ReserveNow


reservation_ns = Namespace(name="testing", validate=True)
reservation_ns.models[ReserveNow.name] = ReserveNow


@reservation_ns.route('/', doc={"description": "Alias for /my-resource/<id>"},)
class reservation(Resource):

    def __init__(self, api=None, *args, **kwargs):
        # sessions is a black box dependency
        self.resMan = kwargs['res_man']
        super().__init__(api, *args, **kwargs)

    @reservation_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'A lot went wrong'},
                        params={'id': 'Specify the Id associated with the person'})
    def get(self):
        '''Get Reservation'''
        return {'message': 'you cant book now'}

    @reservation_ns.doc('create_reservation')
    @reservation_ns.expect(ReserveNow)
    @reservation_ns.marshal_with(ReserveNow, code=201)
    def post(self):
        '''Create a new reservation'''
        return self.resMan.create(reservation_ns.payload), 201


@reservation_ns.route('/<float:price>')
# @reservation_ns.response(404, 'Not found')
# @reservation_ns.param('price', 'The given Price')
class reservation2(Resource):
    def __init__(self, api=None, *args, **kwargs):
        # sessions is a black box dependency
        self.resMan = kwargs['res_man']
        super().__init__(api, *args, **kwargs)

    '''Get Price for reservation'''
    @reservation_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'A lot went wrong'})
    def get(self, price):
        '''Get Price for Reservation'''
        p = {}
        p['price'] = price
        return self.resMan.create(p), 200