#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:57:33 2021

@author: maurer

Starter class for pyOCPI test
"""

import json
import os
import logging
from ocpi import createOcpiBlueprint
import ocpi.managers as om
from flask import Flask, redirect


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('ocpi')

app = Flask(__name__)
app.config['RESTX_MASK_SWAGGER'] = False


@app.route('/', methods=['POST', 'GET'])
def home():
    return redirect('/ocpi/ui')


cred_roles = [{
    'role': 'HUB',
    'business_details': {
        'name': 'SmartChargingHub',
        'website': 'https://fh-aachen.de',
        'logo': {
            'url': 'https://upload.wikimedia.org/wikipedia/commons/5/5b/FHAachen-logo2010.svg',
            'category': 'OPERATOR',
            'type': 'svg'
        },
    },
    'party_id': 'FHA',
    'country_code': 'DE'}]

# inject dependencies here
# must be as expected
ses = om.SessionManager()
loc = om.LocationManager()
commands = om.CommandsManager()
reservations = om.ReservationManager()
HOST_URL = os.getenv('HOST_URL', "http://localhost:5000")+"/ocpi/"
# TODO maybe provide interface and inject with decorator..?
cm = om.CredentialsDictMan(cred_roles, HOST_URL)
injected_objects = {
    'credentials': cm,
    # 'locations': loc,
    # 'commands': commands,
    'sessions': ses,
    # 'reservations': reservations,
    'parking': reservations,
}

config = 'ocpi.json'
if os.path.exists(config):
    log.info(f'reading config file {config}')
    with open(config, 'r') as f:
        conf = json.load(f)
        cm._updateToken(conf['token'], None, None)
        cm.credentials_roles[0]['business_details']['name']=conf['name']
else:
    log.info(f'config file {config} does not exist')
    cm._updateToken('TESTTOKEN', None, None)

blueprint = createOcpiBlueprint(
    HOST_URL, injected_objects, roles=['RECEIVER'])
app.register_blueprint(blueprint)

if __name__ == '__main__':

    app.run()