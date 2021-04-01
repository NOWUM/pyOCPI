#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:57:33 2021

@author: maurer

Starter class for pyOCPI test
"""

from ocpi import createOcpiBlueprint
from ocpi.managers import cm, SessionManager, LocationManager, ReservationManager, CommandsManager


if __name__ == '__main__':

    from flask import Flask, redirect
    app = Flask(__name__)
    app.config['RESTX_MASK_SWAGGER'] = False

    @app.route('/', methods=['POST', 'GET'])
    def home():
        return redirect('/ocpi/v2/ui')

    # inject dependencies here
    # must be as expected
    ses = SessionManager()
    res = ReservationManager()
    loc = LocationManager()
    commands = CommandsManager()
    injected_objects = {'db': 'db_test',
                        'session_manager': ses,
                        'res_man': res,
                        'location_manager': loc,
                        'credentials_manager': cm,
                        'commands_manager': commands,
                        }

    blueprint = createOcpiBlueprint(injected_objects)
    app.register_blueprint(blueprint)

    app.run()