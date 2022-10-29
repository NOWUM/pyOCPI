"""
Created on Wed June 09 2021
https://github.com/ocpi/ocpi/blob/master/mod_cdrs.asciidoc
@author: gruell
"""

from flask_restx import fields, Model
from ocpi.models.location import connector_type, connector_format, power_type, GeoLocation
from ocpi.models.tokens import token_type
from ocpi.models.tariffs import Price, Tariff, add_models_to_tariffs_namespace
from ocpi.models.types import CaseInsensitiveString

# Enums:
auth_method = ['AUTH_REQUEST', 'COMMAND', 'WHITELIST']  # AuthMethod
cdr_dimension_type = ['CURRENT', 'ENERGY', 'ENERGY_EXPORT', 'ENERGY_IMPORT', 'MAX_CURRENT', 'MIN_CURRENT',
                      'MAX_POWER', 'MIN_POWER', 'PARKING_TIME', 'POWER', 'RESERVATION_TIME', 'STATE_OF_CHARGE', 'TIME']  # CdrDimensionType

# Classes:
CdrDimension = Model('CdrDimension', {
    'type': fields.String(enum=cdr_dimension_type, required=True, description='Type of CDR dimension.'),
    'volume': fields.Float(required=True, description='Volume of the dimension consumed, measured according to the dimension type.')
})

CdrLocation = Model('CdrLocation', {
    'id': CaseInsensitiveString(max_length=36, required=True, description='Uniquely identifies the location within the CPO’s platform (and suboperator platforms). This field can never be changed, modified or renamed.'),
    'name': fields.String(max_length=255, required=False, description='Display name of the location.'),
    'address': fields.String(max_length=45, required=True, description='Street/block name and house number if available.'),
    'city': fields.String(max_length=45, required=True, description='City or town.'),
    'postal_code': fields.String(max_length=10, required=True, description='Postal code of the location.'),
    'country': fields.String(max_length=3, required=True, description='ISO 3166-1 alpha-3 code for the country of this location.'),
    'coordinates': fields.Nested(GeoLocation, required=True, description='Coordinates of the location.'),
    'evse_uid': CaseInsensitiveString(max_length=36, required=True, description='Uniquely identifies the EVSE within the CPO’s platform (and suboperator platforms). For example a database unique ID or the actual EVSE ID. This field can never be changed, modified or renamed. This is the technical identification of the EVSE, not to be used as human readable identification, use the field: evse_id for that.'),
    'evse_id': CaseInsensitiveString(max_length=48, required=True, description='Compliant with the following specification for EVSE ID from "eMI3 standard version V1.0" (http://emi3group.com/documents-links/) "Part 2: business objects.".'),
    'connector_id': CaseInsensitiveString(max_length=36, required=False, description='Identifier of the connector within the EVSE.'),
    'connector_standard': fields.String(enum=connector_type, required=True, description='The standard of the installed connector.'),
    'connector_format': fields.String(enum=connector_format, required=True, description='The format (socket/cable) of the installed connector.'),
    'connector_power_type': fields.String(enum=power_type, required=True, description='')
})

CdrToken = Model('CdrToken', {
    'country_code': CaseInsensitiveString(max_length=2, required=True, description='ISO-3166 alpha-2 country code of the CPO that "owns" this CDR.'),
    'party_id': CaseInsensitiveString(max_length=3, required=True, description='CPO ID of the CPO that "owns" this CDR (following the ISO-15118 standard).'),
    'uid': CaseInsensitiveString(max_length=36, required=True, description='''Unique ID by which this Token can be identified.
                         This is the field used by the CPO’s system (RFID reader on the Charge Point) to identify this token.
                         Currently, in most cases: type=RFID, this is the RFID hidden ID as read by the RFID reader, but that is not a requirement.
                         If this is a type=APP_USER Token, it will be a unique, by the eMSP, generated ID.'''),
    'type': fields.String(enum=token_type, required=True, description='Type of the token'),
    'contract_id': CaseInsensitiveString(max_length=36, required=True, description='Uniquely identifies the EV driver contract token within the eMSP’s platform (and suboperator platforms). Recommended to follow the specification for eMA ID from "eMI3 standard version V1.0" (http://emi3group.com/documents-links/) "Part 2: business objects."')
})

ChargingPeriod = Model('ChargingPeriod', {
    'start_date_time': fields.DateTime(required=True, description='Start timestamp of the charging period. A period ends when the next period starts. The last period ends when the session ends.'),
    'dimensions': fields.List(fields.Nested(CdrDimension), required=True, description='List of relevant values for this charging period.'),
    'tariff_id': CaseInsensitiveString(max_length=36, required=False, description='Unique identifier of the Tariff that is relevant for this Charging Period. If not provided, no Tariff is relevant during this period.')
})

SignedValue = Model('SignedValue', {
    'nature': CaseInsensitiveString(max_length=32, required=True, description='''Nature of the value, in other words, the event this value belongs to.
                            Possible values at moment of writing:
                            - Start (value at the start of the Session)
                            - End (signed value at the end of the Session)
                            - Intermediate (signed values take during the Session, after Start, before End)
                            Others might be added later.'''),
    'plain_data': fields.String(max_length=512, required=True, description='The unencoded string of data. The format of the content depends on the EncodingMethod field.'),
    'signed_data': fields.String(max_length=512, required=True, description='Blob of signed data, base64 encoded. The format of the content depends on the EncodingMethod field.')
})

SignedData = Model('SignedData', {
    'encoding_method': CaseInsensitiveString(max_length=36, required=True, description='The name of the encoding used in the SignedData field. This is the name given to the encoding by a company or group of companies. See note below.'),
    'encoding_method_version': fields.Integer(required=False, description='Version of the EncodingMethod (when applicable)'),
    'public_key': fields.String(max_length=512, required=False, description='Public key used to sign the data, base64 encoded.'),
    'signed_values': fields.List(fields.Nested(SignedValue), required=True, description='One or more signed values.'),
    'url': fields.String(max_length=512, required=False, description='URL that can be shown to an EV driver. This URL gives the EV driver the possibility to check the signed data from a charging session.')
})

# Objects:
Cdr = Model('Cdr', {
    'country_code': CaseInsensitiveString(max_length=2, required=True, description='ISO-3166 alpha-2 country code of the CPO that "owns" this CDR.'),
    'party_id': CaseInsensitiveString(max_length=3, required=True, description='CPO ID of the CPO that "owns" this CDR (following the ISO-15118 standard).'),
    'id': CaseInsensitiveString(max_length=39, required=True, description='Uniquely identifies the CDR within the CPO’s platform (and suboperator platforms). This field is longer than the usual 36 characters to allow for credit CDRs to have something appended to the original ID. Normal (non-credit) CDRs SHALL only have an ID with a maximum length of 36.'),
    'start_date_time': fields.DateTime(required=True, description='Start timestamp of the charging session, or in-case of a reservation (before the start of a session) the start of the reservation.'),
    'end_date_time': fields.DateTime(required=True, description='The timestamp when the session was completed/finished, charging might have finished before the session ends, for example: EV is full, but parking cost also has to be paid.'),
    'session_id': CaseInsensitiveString(max_length=36, required=False, description='Unique ID of the Session for which this CDR is sent. Is only allowed to be omitted when the CPO has not implemented the Sessions module or this CDR is the result of a reservation that never became a charging session, thus no OCPI Session.'),
    'cdr_token': fields.Nested(CdrToken, required=True, description='Token used to start this charging session, includes all the relevant information to identify the unique token.'),
    'auth_method': fields.String(enum=auth_method, required=True, description='Method used for authentication.'),
    'authorization_reference': CaseInsensitiveString(max_length=36, required=False, description='Reference to the authorization given by the eMSP. When the eMSP provided an authorization_reference in either: real-time authorization or StartSession, this field SHALL contain the same value. When different authorization_reference values have been given by the eMSP that are relevant to this Session, the last given value SHALL be used here.'),
    'cdr_location': fields.Nested(CdrLocation, required=True, description='Location where the charging session took place, including only the relevant EVSE and Connector.'),
    'meter_id': fields.String(max_length=255, required=False, description='Identification of the Meter inside the Charge Point.'),
    'currency': fields.String(max_length=3, required=True, description='Currency of the CDR in ISO 4217 Code.'),
    'tariffs': fields.List(fields.Nested(Tariff), required=False, description='List of relevant Tariff Elements, see: Tariff. When relevant, a Free of Charge tariff should also be in this list, and point to a defined Free of Charge Tariff.'),
    'charging_periods': fields.List(fields.Nested(ChargingPeriod), required=True, description='List of Charging Periods that make up this charging session. A session consists of 1 or more periods, where each period has a different relevant Tariff.'),
    'signed_data': fields.Nested(SignedData, required=False, description='Signed data that belongs to this charging Session.'),
    'total_cost': fields.Nested(Price, required=True, description='Total sum of all the costs of this transaction in the specified currency.'),
    'total_fixed_cost': fields.Nested(Price, required=False, description='Total sum of all the fixed costs in the specified currency, except fixed price components of parking and reservation. The cost not depending on amount of time/energy used etc. Can contain costs like a start tariff.'),
    'total_energy': fields.Float(required=True, description='Total energy charged, in kWh.'),
    'total_energy_cost': fields.Nested(Price, required=False, description='Total sum of all the cost of all the energy used, in the specified currency.'),
    'total_time': fields.Float(required=True, description='Total duration of the charging session (including the duration of charging and not charging), in hours.'),
    'total_time_cost': fields.Nested(Price, required=False, description='Total sum of all the cost related to duration of charging during this transaction, in the specified currency.'),
    'total_parking_time': fields.Float(required=False, description='Total duration of the charging session where the EV was not charging (no energy was transferred between EVSE and EV), in hours.'),
    'total_parking_cost': fields.Nested(Price, required=False, description='Total sum of all the cost related to parking of this transaction, including fixed price components, in the specified currency.'),
    'total_reservation_cost': fields.Nested(Price, required=False, description='Total sum of all the cost related to a reservation of a Charge Point, including fixed price components, in the specified currency.'),
    'remark': fields.String(max_length=255, required=False, description='Optional remark, can be used to provide additional human readable information to the CDR, for example: reason why a transaction was stopped.'),
    'invoice_reference_id': CaseInsensitiveString(max_length=39, required=False, description='This field can be used to reference an invoice, that will later be send for this CDR. Making it easier to link a CDR to a given invoice. Maybe even group CDRs that will be on the same invoice.'),
    'credit': fields.Boolean(required=False, description='When set to true, this is a Credit CDR, and the field credit_reference_id needs to be set as well.'),
    'credit_reference_id': CaseInsensitiveString(max_length=39, required=False, description='Is required to be set for a Credit CDR. This SHALL contain the id of the CDR for which this is a Credit CDR.'),
    'last_updated': fields.DateTime(required=True, description='Timestamp when this CDR was last updated (or created).')
})


def add_models_to_cdr_namespace(namespace):
    add_models_to_tariffs_namespace(namespace)
    for model in [Cdr, SignedData, SignedValue, ChargingPeriod, CdrToken,
                  CdrLocation, CdrDimension, ]:
        namespace.models[model.name] = model