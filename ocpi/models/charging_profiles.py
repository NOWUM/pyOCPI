"""
Created on Thu May 26 2021
https://github.com/ocpi/ocpi/blob/master/mod_charging_profiles.asciidoc
@author: gruell
"""

from flask_restx import Model, fields

# Enums:
charging_profile_response_type = ['ACCEPTED', 'NOT_SUPPORTED', 'REJECTED', 'TOO_OFTEN', 'UNKNOWN_SESSION'] #ChargingProfileResponseType
charging_profile_result_type = ['ACCEPTED', 'REJECTED', 'UNKNOWN'] #ChargingProfileResultType
charging_rate_unit = ['W', 'A'] #ChargingRateUnit

# Classes:
ChargingProfilePeriod = Model('ChargingProfilePeriod', {
    'start_period': fields.Integer(required=True, description='Start of the period, in seconds from the start of profile. The value of StartPeriod also defines the stop time of the previous period.'),
    'limit': fields.Float(required=True, description='Charging rate limit during the profile period, in the applicable chargingRateUnit, for example in Amperes (A) or Watts (W). Accepts at most one digit fraction (e.g. 8.1).')
})

ChargingProfile = Model('ChargingProfile', {
    'start_date_time': fields.DateTime(required=False, description='Starting point of an absolute profile. If absent the profile will be relative to start of charging.'),
    'duration': fields.Integer(required=False, description='Duration of the charging profile in seconds. If the duration is left empty, the last period will continue indefinitely or until end of the transaction in case startProfile is absent.'),
    'charging_rate_unit': fields.String(enum=charging_rate_unit, required=True, description='The unit of measure.'),
    'min_charging_rate': fields.Float(required=False, description='Minimum charging rate supported by the EV. The unit of measure is defined by the chargingRateUnit. This parameter is intended to be used by a local smart charging algorithm to optimize the power allocation for in the case a charging process is inefficient at lower charging rates. Accepts at most one digit fraction (e.g. 8.1)'),
    'charging_profile_period': fields.List(fields.Nested(ChargingProfilePeriod), required=False, description='List of ChargingProfilePeriod elements defining maximum power or current usage over time.')
})

ActiveChargingProfile = Model('ActiveChargingProfile', {
    'start_date_time': fields.DateTime(required=True, description='Date and time at which the Charge Point has calculated this ActiveChargingProfile. All time measurements within the profile are relative to this timestamp.'),
    'charging_profile': fields.Nested(ChargingProfile, required=True, description='Charging profile structure defines a list of charging periods.')
})

# Objects:
ChargingProfileResponse = Model('ChargingProfileResponse', {
    'result': fields.String(enum=charging_profile_response_type, required=True, description='Response from the CPO on the ChargingProfile request.'),
    'timeout': fields.Integer(required=True, description='Timeout for this ChargingProfile request in seconds. When the Result is not received within this timeout, the eMSP can assume that the message might never be sent.')
})

ActiveChargingProfileResult = Model('ActiveChargingProfileResult', {
    'result': fields.String(enum=charging_profile_result_type, required=True, description='The EVSE will indicate if it was able to process the request for the ActiveChargingProfile'),
    'profile': fields.Nested(ActiveChargingProfile, required=False, description='The requested ActiveChargingProfile, if the result field is set to: ACCEPTED')
})

ChargingProfileResult = Model('ChargingProfileResult', {
    'result': fields.String(enum=charging_profile_result_type, required=True, description='The EVSE will indicate if it was able to process the new/updated charging profile.')
})

ClearProfileResult = Model('ClearProfileResult', {
    'result': fields.String(enum=charging_profile_result_type, required=True, description='The EVSE will indicate if it was able to process the removal of the charging profile (ClearChargingProfile).')
})

SetChargingProfile = Model('SetChargingProfile', {
    'charging_profile': fields.Nested(ChargingProfile, required=True, description='Contains limits for the available power or current over time.'),
    'response_url': fields.String(required=True, description='URL that the ChargingProfileResult POST should be send to. This URL might contain an unique ID to be able to distinguish between GET ActiveChargingProfile requests.')
})

def add_models_to_charging_profiles_namespace(namespace):
    for model in [SetChargingProfile, ClearProfileResult, ChargingProfileResult, ActiveChargingProfileResult, ChargingProfileResponse, ActiveChargingProfile, ChargingProfile, ChargingProfilePeriod]:
        namespace.models[model.name] = model