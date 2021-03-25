#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:57:33 2021

@author: maurer

Starter class for pyOCPI test
"""

from ocpi import createBlueprint


class SessionManager(object):

    def __init__(self):
        self.sessions = {}


class ReservationManager(object):

    def __init__(self):
        self.reservations = []

    def create(self, payload):
        self.reservations.append(payload)
        return payload['price']*1.19+3


if __name__ == '__main__':

    from flask import Flask, redirect
    app = Flask(__name__)

    @app.route('/', methods=['POST', 'GET'])
    def home():
        return redirect('/api/v1/ui')

    # inject dependencies here
    # must be as expected
    ses = SessionManager()
    res = ReservationManager()
    injected_objects = {'db': 'db_test',
                        'session_manager': ses, 'res_man': res}

    blueprint = createBlueprint(injected_objects)
    app.register_blueprint(blueprint)

    app.run()
