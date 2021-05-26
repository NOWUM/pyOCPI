"""
Created on Thu May 26 2021
https://github.com/ocpi/ocpi/blob/master/mod_charging_profiles.asciidoc
@author: gruell
"""
#TODO: fill empty models

from flask_restx import Model, fields

# Enums:
charging_profile_response_type = ['ACCEPTED', 'NOT_SUPPORTED', 'REJECTED', 'TOO_OFTEN', 'UNKNOWN_SESSION'] #ChargingProfileResponseType
charging_profile_result_type = ['ACCEPTED', 'REJECTED', 'UNKNOWN'] #ChargingProfileResultType
charging_rate_unit = ['W', 'A'] #ChargingRateUnit

# Classes:
ActiveChargingProfile = Model('ActiveChargingProfile', {

})

ChargingProfile = Model('ChargingProfile', {

})

ChargingprofilePeriod = Model('ChargingprofilePeriod', {

})

# Objects:
ChargingProfileResponse = Model('ChargingProfileResponse', {
    'result': fields.Nested(charging_profile_response_type, required=True, description='Response from the CPO on the ChargingProfile request.'),
    'timeout': fields.Integer(required=True, description='Timeout for this ChargingProfile request in seconds. When the Result is not received within this timeout, the eMSP can assume that the message might never be sent.')
})

ActiveChargingProfileResult = Model('ActiveChargingProfileResult', {
    'result': fields.Nested(charging_profile_result_type, required=True, description='The EVSE will indicate if it was able to process the request for the ActiveChargingProfile'),
    'profile': fields.Nested(ActiveChargingProfile, required=False, description='The requested ActiveChargingProfile, if the result field is set to: ACCEPTED')
})

ChargingProfileResult = Model('ChargingProfileResult', {

})

ClearProfileResult = Model('ClearProfileResult', {

})

SetChargingProfile = Model('SetChargingProfile', {

})

