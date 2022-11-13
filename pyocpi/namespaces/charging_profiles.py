"""
Created on Thu May 26 2021
https://github.com/ocpi/ocpi/blob/master/mod_charging_profiles.asciidoc
@author: gruell
"""

import logging
from flask_restx import Resource, Namespace
from flask_restx import reqparse
from ocpi.models import resp

from ocpi.models.charging_profiles import (add_models_to_charging_profiles_namespace,
                                           ChargingProfileResponse, SetChargingProfile,
                                           ActiveChargingProfile, ActiveChargingProfileResult,
                                           ChargingProfileResult, ClearProfileResult)
from ocpi.namespaces import get_header_parser, token_required, make_response

charging_profiles_ns = Namespace(name="tariffs", validate=True)

add_models_to_charging_profiles_namespace(charging_profiles_ns)
parser = get_header_parser(charging_profiles_ns)

log = logging.getLogger('ocpi')

# (https://github.com/ocpi/ocpi/blob/master/mod_tariffs.asciidoc#122-receiver-interface)


def receiver():
    @charging_profiles_ns.route('/<string:session_id>')
    @charging_profiles_ns.expect(parser)
    class manage_charging_profiles(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        @charging_profiles_ns.marshal_with(resp(charging_profiles_ns, ChargingProfileResponse))
        @token_required
        def get(self, session_id):
            '''
            Gets the ActiveChargingProfile for a specific charging session.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('duration', type=int)
            parser.add_argument('response_url', type=str)
            args = parser.parse_args()
            return make_response(self.chargingprofilesmanager.getChargingProfile,
                                 session_id, args['duration'], args['response_url'])

        @charging_profiles_ns.expect(SetChargingProfile)
        @charging_profiles_ns.marshal_with(resp(charging_profiles_ns, ChargingProfileResponse))
        @token_required
        def put(self, session_id):
            '''
            Creates/updates a ChargingProfile for a specific charging session.
            '''
            return make_response(self.chargingprofilesmanager.putChargingProfile,
                                 session_id, charging_profiles_ns.payload)

        @charging_profiles_ns.marshal_with(resp(charging_profiles_ns, ChargingProfileResponse))
        @token_required
        def delete(self, session_id):
            '''
            Cancels an existing ChargingProfile for a specific charging session.
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('response_url', type=str)
            args = parser.parse_args()
            return make_response(self.chargingprofilesmanager.deleteChargingProfile,
                                 session_id, args['response_url'])


def sender():
    # There are no URL segment parameters required by OCPI.
    @charging_profiles_ns.route('/active_charging_profile_result/<string:session_id>')
    class active_charging_profile_result(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        @charging_profiles_ns.expect(ActiveChargingProfileResult)
        @token_required
        def post(self, session_id):
            return make_response(self.chargingprofilesmanager.handleActiveChargingProfileResult,
                                 session_id, charging_profiles_ns.payload)

    @charging_profiles_ns.route('/charging_profile_result/<string:session_id>')
    class charging_profile_result(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        @charging_profiles_ns.expect(ChargingProfileResult)
        @token_required
        def post(self, session_id):
            return make_response(self.chargingprofilesmanager.handleChargingProfileResult,
                                 session_id, charging_profiles_ns.payload)

    @charging_profiles_ns.route('/clear_profile_result/<string:session_id>')
    class clear_profile_result(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        @charging_profiles_ns.expect(ClearProfileResult)
        @token_required
        def post(self, session_id):
            return make_response(self.chargingprofilesmanager.handleClearProfileResult,
                                 session_id, charging_profiles_ns.payload)

    @charging_profiles_ns.route('/<string:session_id>')
    class update_sender_active_charging_profile(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.chargingprofilesmanager = kwargs['charging_profiles']
            super().__init__(api, *args, **kwargs)

        @charging_profiles_ns.expect(ActiveChargingProfile)
        def put(self, session_id):
            # should only be sent if the sender received a post to SetChargingProfile
            # Updates the Sender (typically SCSP) when the Receiver (typically CPO) knows the ActiveChargingProfile has changed.
            return make_response(self.chargingprofilesmanager.handleUpdateActiveChargingProfile,
                                 session_id, charging_profiles_ns.payload)


def makeChargingProfilesNamespace(role):
    if role == 'SENDER':
        sender()
    elif role == 'RECEIVER':
        receiver()
    else:
        raise Exception('invalid role')

    return charging_profiles_ns