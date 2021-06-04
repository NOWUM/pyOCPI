"""
Created on Thu May 26 2021
https://github.com/ocpi/ocpi/blob/master/mod_charging_profiles.asciidoc
@author: gruell
"""
#TODO: implement charging_profile namespace
# - add missing functions for receiver and sender


import logging
from flask_restx import Resource, Namespace
from flask_restx import reqparse
from flask_restx.inputs import datetime_from_iso8601
from ocpi.models import resp, respList
from ocpi.decorators import get_header_parser, token_required
from ocpi.models.charging_profiles import add_models_to_charging_profiles_namespace, ChargingProfileResponse
from datetime import datetime

charging_profiles_ns = Namespace(name="tariffs", validate=True)

add_models_to_charging_profiles_namespace(charging_profiles_ns)
parser = get_header_parser(charging_profiles_ns)

log = logging.getLogger('ocpi')

#(https://github.com/ocpi/ocpi/blob/master/mod_tariffs.asciidoc#122-receiver-interface)
def receiver():
    @charging_profiles_ns.route('/<string:session_id>')
    @charging_profiles_ns.expect(parser)
    class manage_charging_profiles(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        @charging_profiles_ns.marshal_with(resp(charging_profiles_ns, ChargingProfileResponse))
        def get(self, session_id):
            '''
            Gets the ActiveChargingProfile for a specific charging session.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('duration', type=int)
            parser.add_argument('response_url', type=str)
            args = parser.parse_args()
            data = self.chargingprofilesmanager.getChargingProfile(session_id, args['duration'], args['response_url'])

            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        def put(self, session_id):
            '''
            Creates/updates a ChargingProfile for a specific charging session.
            '''
            pass

        def delete(self, session_id):
            '''
            Cancels an existing ChargingProfile for a specific charging session.
            '''
            pass

def sender():
    class find_class_name(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        def post(self):
            #There are no URL segment parameters required by OCPI.
            #request body: Choice: one of three (ActiveChargingProfileResult, ChargingProfileResult, ClearProfileResult)
            pass

        def put(self, session_id):
            pass


def makeChargingProfilesNamespace(interfaces=['SENDER', 'RECEIVER']):
    log.debug('charging profiles interfaces:'+str(interfaces))
    if 'SENDER' in interfaces:
        sender()
    if 'RECEIVER' in interfaces:
        receiver()

    return charging_profiles_ns