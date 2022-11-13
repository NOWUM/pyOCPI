#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:13:00 2021
https://github.com/ocpi/ocpi/blob/master/mod_tokens.asciidoc
@author: gruell
"""

from flask_restx import fields, Model

from ocpi.models.types import CaseInsensitiveString

# Enums:
allowed_type = ["ALLOWED", "BLOCKED", "EXPIRED", "NO_CREDIT", "NOT_ALLOWED"] # AllowedType
token_type = ["AD_HOC_USER", "APP_USER", "OTHER", "RFID"] # TokenType
whitelist_type = ["ALWAYS", "ALLOWED", "ALLOWED_OFFLINE", "NEVER"] # WhitelistType
profile_type = ["CHEAP", "FAST", "GREEN", "REGULAR"] # ProfileType

# Classes:
EnergyContract = Model('EnergyContract', {
    'supplier_name': fields.String(max_length=64, required=True, description='Name of the energy supplier for this token.'),
    'contract_id': fields.String(max_length=64, required=False, description='Contract ID at the energy supplier, that belongs to the owner of this token.')
})

LocationReferences = Model('LocationReferences', {
    'location_id': CaseInsensitiveString(max_length=36, required=True, description='Unique identifier for the location.'),
    'evse_uids': fields.List(CaseInsensitiveString(max_length=36), required=False, description='Unique identifiers for EVSEs within the CPO’s platform for the EVSE within the given location.')
})

DisplayText = Model('DisplayText', {
    'language': fields.String(max_length=2, required=True, description='Language Code ISO 639-1.'),
    'text': fields.String(max_length=512, required=True, description='Text to be displayed to a end user. No markup, html etc. allowed.')
})

# Objects:
Token = Model('Token', {
    'country_code': CaseInsensitiveString(max_length=2, required=True, description="ISO-3166 alpha-2 country code of the MSP that 'owns' this Token."),
    'party_id': CaseInsensitiveString(max_length=3, required=True, description="CPO ID of the MSP that 'owns' this Token (following the ISO-15118 standard)."),
    'uid': CaseInsensitiveString(max_length=36, required=True, description='Unique ID by which this Token can be identified.'
                                                                    'This is the field used by CPO system (RFID reader on the Charge Point) to identify this token.'
                                                                    'Currently, in most cases: type=RFID, this is the RFID hidden ID as read by the RFID reader, but that is not a requirement.'
                                                                    'If this is a APP_USER or AD_HOC_USER Token, it will be a uniquely, by the eMSP, generated ID.'
                                                                    'This field is named uid instead of id to prevent confusion with: contract_id.'),
    'type': fields.String(enum=token_type, required=True, description='Type of the token'),
    'contract_id': CaseInsensitiveString(max_length=36, required=True, description='Uniquely identifies the EV Driver contract token within the eMSP’s platform (and suboperator platforms). Recommended to follow the specification for eMA ID from "eMI3 standard version V1.0" (http://emi3group.com/documents-links/) "Part 2: business objects."'),
    'visual_number': fields.String(max_length=64, required=False, description='Visual readable number/identification as printed on the Token (RFID card), might be equal to the contract_id.'),
    'issuer': fields.String(max_length=64, required=True, description='Issuing company, most of the times the name of the company printed on the token (RFID card), not necessarily the eMSP.'),
    'group_id': CaseInsensitiveString(max_length=36, required=False, description='This ID groups a couple of tokens. This can be used to make two or more tokens work as one, so that a session can be started with one token and stopped with another, handy when a card and key-fob are given to the EV-driver.'
                                                                         'Beware that OCPP 1.5/1.6 only support group_ids (it is called parentId in OCPP 1.5/1.6) with a maximum length of 20.'),
    'valid': fields.Boolean(required=True,description='Is this Token valid'),
    'whitelist': fields.String(enum=whitelist_type, required=True, description='Indicates what type of white-listing is allowed.'),
    'language': fields.String(max_length=2, required=False, description='Language Code ISO 639-1. This optional field indicates the Token owner’s preferred interface language. If the language is not provided or not supported then the CPO is free to choose its own language.'),
    'default_profile_type': fields.String(enum=profile_type, required=False, description='The default Charging Preference. When this is provided, and a charging session is started on an Charge Point that support Preference base Smart Charging and support this ProfileType, the Charge Point can start using this ProfileType, without this having to be set via: Set Charging Preferences.'),
    'energy_contract': fields.Nested(EnergyContract, required=False, description='When the Charge Point supports using your own energy supplier/contract at a Charge Point, information about the energy supplier/contract is needed so the CPO knows which energy supplier to use.'
                                                                                 'NOTE: In a lot of countries it is currently not allowed/possible to use a drivers own energy supplier/contract at a Charge Point.'),
    'last_updated': fields.DateTime(required=True, description='Timestamp when this Token was last updated (or created).')
})

AuthorizationInfo = Model('AuthorizationInfo', {
    'allowed': fields.String(enum=allowed_type, required=True, description='Status of the Token, and whether charging is allowed at the optionally given location.'),
    'token': fields.Nested(Token, required=True, description='The complete Token object for which this authorization was requested.'),
    'location': fields.Nested(LocationReferences, required=False, description='Optional reference to the location if it was included in the request, and if the EV driver is allowed to charge at that location. Only the EVSEs the EV driver is allowed to charge at are returned.'),
    'authorization_reference': CaseInsensitiveString(max_length=36, required=False, description='Reference to the authorization given by the eMSP, when given, this reference will be provided in the relevant Session and/or CDR.'),
    'info': fields.Nested(DisplayText, required=False, description='Optional display text, additional information to the EV driver.')
})


def add_models_to_tokens_namespace(namespace):
    for model in [Token, AuthorizationInfo, DisplayText, LocationReferences, EnergyContract]:
        namespace.models[model.name] = model