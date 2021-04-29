#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:57:33 2021

@author: maurer

Starter class for pyOCPI test
"""

from ocpi import createOcpiBlueprint
from ocpi.managers import CredentialsManager, ReservationManager, SessionManager, LocationManager, CommandsManager
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
reservations = ReservationManager()
base_url = "http://localhost:5000/ocpi/v2"
# TODO maybe provide interface and inject with decorator..?
cm = CredentialsManager(cred_role, base_url)
injected_objects = {
    'credentials': cm,
    'locations': loc,
    'versions': ses,
    'commands': commands,
    'sessions': ses,
    'reservations': reservations,
    'parking': reservations,
}

blueprint = createOcpiBlueprint(
    base_url, injected_objects, roles=['RECEIVER'])
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run()