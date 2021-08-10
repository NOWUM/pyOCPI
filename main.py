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


# country_code, party_id and role is "username"
# token is "password"
# "username" and "password" must be communicated "out of band" (per mail or so)
# multiple roles could be implemented simultanously
cred_roles = [{
    'role': 'CPO',
    'business_details': {
        'name': 'pyOCPI example',
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
    'credentials': {'role': 'SENDER', 'object': cm},
    'locations': {'role': 'SENDER', 'object': loc},
    'commands': {'role': 'SENDER', 'object': commands},
    'sessions': {'role': 'SENDER', 'object': ses},
    'reservations': {'role': 'SENDER', 'object': reservations},
    'tokens': {'role': 'SENDER', 'object': om.TokensManager()},
    'tariffs': {'role': 'SENDER', 'object': om.TariffsManager()},
    'charging_profiles': {'role': 'SENDER', 'object': om.ChargingProfilesManager()},
    'cdrs': {'role': 'SENDER', 'object': om.CdrManager()},
}

config = 'ocpi.json'
if os.path.exists(config):
    log.info(f'reading config file {config}')
    with open(config, 'r') as f:
        conf = json.load(f)
        cm._updateToken(conf['token'], None, None, endpoint_list=[])
        cm.credentials_roles[0]['business_details']['name'] = conf['name']
        cm.credentials_roles[0]['party_id'] = conf['party_id']
        cm.credentials_roles[0]['country_code'] = conf['country_code']
else:
    log.info(f'config file {config} does not exist')
    cm._updateToken('TESTTOKEN', None, None)

blueprint = createOcpiBlueprint(
    HOST_URL, injected_objects)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run()