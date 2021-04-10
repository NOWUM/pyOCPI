#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:57:33 2021

@author: maurer

Starter class for pyOCPI test
"""

from ocpi import createOcpiBlueprint
from ocpi.managers import CredentialsManager, SessionManager, LocationManager, CommandsManager

if __name__ == '__main__':

    from flask import Flask, redirect
    app = Flask(__name__)
    app.config['RESTX_MASK_SWAGGER'] = False

    @app.route('/', methods=['POST', 'GET'])
    def home():
        return redirect('/ocpi/v2/ui')

    cred_role = {'role': 'HUB',
                 'business_details': {
                     'name': 'SmartChargingHub',
                     'website': 'https://fh-aachen.de',
                     # 'logo': ,
                 },
                 'party_id': 'SCH',
                 'country_code': 'DE'}

    # inject dependencies here
    # must be as expected
    ses = SessionManager()
    loc = LocationManager()
    commands = CommandsManager()
    base_url = "http://localhost:5000"
    cm = CredentialsManager(cred_role, base_url)
    injected_objects = {'db': 'db_test',
                        'session_manager': ses,
                        'location_manager': loc,
                        'credentials_manager': cm,
                        'command_manager': commands,
                        }

    blueprint = createOcpiBlueprint(injected_objects)
    app.register_blueprint(blueprint)

    app.run()