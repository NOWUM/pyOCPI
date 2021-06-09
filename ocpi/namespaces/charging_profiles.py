"""
Created on Thu May 26 2021
https://github.com/ocpi/ocpi/blob/master/mod_charging_profiles.asciidoc
@author: gruell
"""

#TODO:
# - check receiver interface
# - finish sender interface (Florian)

import logging
from flask_restx import Resource, Namespace
from flask_restx import reqparse
from flask_restx.inputs import datetime_from_iso8601
from ocpi.models import resp, respList
from ocpi.decorators import get_header_parser, token_required
from ocpi.models.charging_profiles import add_models_to_charging_profiles_namespace, ChargingProfileResponse, SetChargingProfile, ActiveChargingProfile, ActiveChargingProfileResult, ChargingProfileResult, ClearProfileResult
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

        @charging_profiles_ns.expect(SetChargingProfile)
        @charging_profiles_ns.marshal_with(resp(charging_profiles_ns, ChargingProfileResponse))
        def put(self, session_id):
            '''
            Creates/updates a ChargingProfile for a specific charging session.
            '''
            data = self.chargingprofilesmanager.putChargingProfile(session_id, charging_profiles_ns.payload)
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        @charging_profiles_ns.marshal_with(resp(charging_profiles_ns, ChargingProfileResponse))
        def delete(self, session_id):
            '''
            Cancels an existing ChargingProfile for a specific charging session.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('response_url', type=str)
            args = parser.parse_args()
            data = self. chargingprofilesmanager.deleteChargingProfile(session_id, args['response_url'])
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

#TODO: sender interface prüfen (hab ich nicht wirklich verstanden)
def sender():
    # There are no URL segment parameters required by OCPI.
    @charging_profiles_ns.route('/active_charging_profile_result/<string:unique_id>')
    class active_charging_profile_result(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        @charging_profiles_ns.expect(ActiveChargingProfileResult)
        def post(self):
            # TODO: Was muss hier gemacht werden?
            return {'data': None,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

    @charging_profiles_ns.route('/charging_profile_result/<string:unique_id>')
    class charging_profile_result(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        @charging_profiles_ns.expect(ChargingProfileResult)
        def post(self):
            #TODO: Was muss hier gemacht werden?
            return {'data': None,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

    @charging_profiles_ns.route('/clear_profile_result/<string:unique_id>')
    class clear_profile_result(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        @charging_profiles_ns.expect(ClearProfileResult)
        def post(self):
            # TODO: Was muss hier gemacht werden?
            return {'data': None,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }


    @charging_profiles_ns.route('/<string:session_id>')
    class update_sender_active_charging_profile(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        @charging_profiles_ns.expect(ActiveChargingProfile)
        def put(self, session_id):
            #Updates the Sender (typically SCSP) when the Receiver (typically CPO) knows the ActiveChargingProfile has changed.
            #self.chargingprofilesmanager.putChargingProfile(session_id) #TODO: muss hier der chargingprofilesmanager auch geupdated werden (wie bei Receiver)?
            return {'data': None,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }


def makeChargingProfilesNamespace(interfaces=['SENDER', 'RECEIVER']):
    log.debug('charging profiles interfaces:'+str(interfaces))
    if 'SENDER' in interfaces:
        sender()
    if 'RECEIVER' in interfaces:
        receiver()

    return charging_profiles_ns