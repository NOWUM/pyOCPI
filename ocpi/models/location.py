#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 23:51:45 2021

@author: maurer
"""

############### Location Models ###############

from flask_restx import fields, Model
from ocpi.models.types import DisplayText, CaseInsensitiveString
from ocpi.models.tokens import token_type

AdditionalGeoLocation = Model('AdditionalGeoLocation', {
    'latitude': fields.String(max_length=10, required=True, description='Latitude of the point in decimal degree.'),
    'longitude': fields.String(max_length=11, required=True, description='Longitude of the point in decimal degree.'),
    'name': fields.Nested(DisplayText, description='Name of the point in local language or as written at the location.')
})

GeoLocation = Model('GeoLocation', {
    'latitude': fields.String(max_length=10, required=True, description='Latitude of the point in decimal degree. Regex: -?[0-9]{1,3}\.[0-9]{5,7}'),
    'longitude': fields.String(max_length=11, required=True, description='Longitude of the point in decimal degree.')
})

capability = [
    'CHARGING_PROFILE_CAPABLE',  # The EVSE supports charging profiles.
    'CHARGING_PREFERENCES_CAPABLE',  # The EVSE supports charging preferences.
    # EVSE has a payment terminal that supports chip cards.
    'CHIP_CARD_SUPPORT',
    # EVSE has a payment terminal that supports contactless cards.
    'CONTACTLESS_CARD_SUPPORT',
    # EVSE has a payment terminal that makes it possible to pay for charging using a credit card.
    'CREDIT_CARD_PAYABLE',
    # EVSE has a payment terminal that makes it possible to pay for charging using a debit card.
    'DEBIT_CARD_PAYABLE',
    # EVSE has a payment terminal with a pin-code entry device.
    'PED_TERMINAL',
    'REMOTE_START_STOP_CAPABLE',  # The EVSE can remotely be started/stopped.
    'RESERVABLE',  # The EVSE can be reserved.
    # Charging at this EVSE can be authorized with an RFID token.
    'RFID_READER',
    # This EVSE supports token groups, two or more tokens work as one, so that a session can be started with one token and stopped with another (handy when a card and key-fob are given to the EV-driver).
    'TOKEN_GROUP_CAPABLE',
    # Connectors have mechanical lock that can be requested by the eMSP to be unlocked.
    'UNLOCK_CAPABLE'
]

connector_type = [
    'CHADEMO'	,  # The connector type is CHAdeMO, DC
    'DOMESTIC_A'	,  # Standard/Domestic household, type "A", NEMA 1-15, 2 pins
    'DOMESTIC_B'	,  # Standard/Domestic household, type "B", NEMA 5-15, 3 pins
    'DOMESTIC_C'	,  # Standard/Domestic household, type "C", CEE 7/17, 2 pins
    'DOMESTIC_D'	,  # Standard/Domestic household, type "D", 3 pin
    'DOMESTIC_E'	,  # Standard/Domestic household, type "E", CEE 7/5 3 pins
    'DOMESTIC_F'	,  # Standard/Domestic household, type "F", CEE 7/4, Schuko, 3 pins
    'DOMESTIC_G'	,  # Standard/Domestic household, type "G", BS 1363, Commonwealth, 3 pins
    'DOMESTIC_H'	,  # Standard/Domestic household, type "H", SI-32, 3 pins
    'DOMESTIC_I'	,  # Standard/Domestic household, type "I", AS 3112, 3 pins
    'DOMESTIC_J'	,  # Standard/Domestic household, type "J", SEV 1011, 3 pins
    'DOMESTIC_K'	,  # Standard/Domestic household, type "K", DS 60884-2-D1, 3 pins
    'DOMESTIC_L'	,  # Standard/Domestic household, type "L", CEI 23-16-VII, 3 pins
    # IEC 60309-2 Industrial Connector single phase 16 amperes (usually blue)
    'IEC_60309_2_single_16'	,
    # IEC 60309-2 Industrial Connector three phase 16 amperes (usually red)
    'IEC_60309_2_three_16'	,
    # IEC 60309-2 Industrial Connector three phase 32 amperes (usually red)
    'IEC_60309_2_three_32'	,
    # IEC 60309-2 Industrial Connector three phase 64 amperes (usually red)
    'IEC_60309_2_three_64'	,
    'IEC_62196_T1'	,  # IEC 62196 Type 1 "SAE J1772"
    'IEC_62196_T1_COMBO'	,  # Combo Type 1 based, DC
    'IEC_62196_T2'	,  # IEC 62196 Type 2 "Mennekes"
    'IEC_62196_T2_COMBO'	,  # Combo Type 2 based, DC
    'IEC_62196_T3A'	,  # IEC 62196 Type 3A
    'IEC_62196_T3C'	,  # IEC 62196 Type 3C "Scame"
    'PANTOGRAPH_BOTTOM_UP'	,  # On-board Bottom-up-Pantograph typically for bus charging
    'PANTOGRAPH_TOP_DOWN'	,  # Off-board Top-down-Pantograph typically for bus charging
    'TESLA_R'	,  # Tesla Connector "Roadster"-type (round, 4 pin)
    'TESLA_S'	,  # Tesla Connector "Model-S"-type (oval, 5 pin)
]

connector_format = ['SOCKET', 'CABLE']

environmental_impact_category = ['NUCLEAR_WASTE', 'CARBON_DIOXIDE']

EnvironmentalImpact = Model('EnvironmentalImpact', {
    'category': fields.String(enum=environmental_impact_category, required=True, description='The environmental impact category of this value.'),
    'amount': fields.Float(required=True, description='Amount of this portion in g/kWh.')
})

energy_source_category = [
    'NUCLEAR'	,  # Nuclear power sources.
    'GENERAL_FOSSIL'	,  # All kinds of fossil power sources.
    'COAL'	,  # Fossil power from coal.
    'GAS'	,  # Fossil power from gas.
    'GENERAL_GREEN'	,  # All kinds of regenerative power sources.
    'SOLAR'	,  # Regenerative power from PV.
    'WIND'	,  # Regenerative power from wind turbines.
    'WATER'	,  # Regenerative power from water turbines.
]

EnergySource = Model('EnergySource', {
    'source': fields.String(enum=energy_source_category, description='The type of energy source.'),
    'percentage': fields.Float(description='Percentage of this source (0-100) in the mix.'),
})

EnergyMix = Model('EnergyMix', {
    'is_green_energy': fields.Boolean(required=True, description='True if 100% from regenerative sources.'),
    'energy_sources': fields.List(fields.Nested(EnergySource)),
    'environ_impact': fields.List(fields.Nested(EnvironmentalImpact)),
    'supplier_name': fields.String(max_length=64, required=True),
    'energy_product_name': fields.String(max_length=64, required=True),
})

power_type = ['AC_1_PHASE', 'AC_3_PHASE', 'DC']

facility = [
    'HOTEL',
    'RESTAURANT',
    'CAFE',
    'MALL',
    'SUPERMARKET',
    'SPORT',
    'RECREATION_AREA',
    'NATURE',
    'MUSEUM',
    'BIKE_SHARING',
    'BUS_STOP',
    'TAXI_STAND',
    'TRAM_STOP',
    'METRO_STATION',
    'TRAIN_STATION',
    'AIRPORT',
    'PARKING_LOT',
    'CARPOOL_PARKING',
    'FUEL_STATION',
    'WIFI'
]

status = [
    'AVAILABLE',
    'BLOCKED',
    'CHARGING',
    'INOPERATIVE',
    'OUTOFORDER',
    'PLANNED',
    'REMOVED',
    'RESERVED',
    'UNKNOWN'
]

parking_restrictions = [
    'EV_ONLY',
    'PLUGGED',
    'DISABLED',
    'CUSTOMERS',
    'MOTORCYCLES'
]

parking_type = [
    'ALONG_MOTORWAY',
    'PARKING_GARAGE',
    'PARKING_LOT',
    'ON_DRIVEWAY',
    'ON_STREET',
    'UNDERGROUND_GARAGE',
]

image_category = [
    'CHARGER',
    'ENTRANCE',
    'LOCATION',
    'NETWORK',
    'OPERATOR',
    'OTHER',
    'OWNER',
]

Image = Model('Image', {
    'url': fields.String(required=True, description='URL from where the image data can be fetched through a web browser.'),
    'thumbnail': fields.String(),
    'category': fields.String(enum=image_category),
    'type': fields.String(max_length=4, required=True, description='Image type like: gif, jpeg, png, svg.'),
    'width': fields.Integer(),
    'height': fields.Integer()
})

BusinessDetails = Model('BusinessDetails', {
    'name': fields.String(max_length=100, required=True, description='Name of the operator'),
    'website': fields.String(description="Link to the operator's website"),
    'logo': fields.Nested(Image, description='Image link to the operator’s logo.'),
})

RegularHours = Model('RegularHours', {
    'weekday': fields.Integer(required=True, description='Number of day in the week, from Monday (1) till Sunday (7)'),
    'period_begin': fields.String(max_length=5, required=True, description='Time; Regex: ([0-1][0-9]|2[0-3]):[0-5][0-9]'),
    'period_end': fields.String(max_length=5, required=True, description='Time; Regex: ([0-1][0-9]|2[0-3]):[0-5][0-9]'),
})

ExceptionalPeriod = Model('ExceptionalPeriod', {
    'period_begin': fields.DateTime(required=True, description='Begin of the exception.'),
    'period_end': fields.DateTime(description='End of the exception.'),
})

PublishTokenType = Model('PublishTokenType', {
    'id': fields.String(max_length=36),
    'type': fields.String(enum=token_type),
    'visual_number': fields.String(max_length=64),
    'issuer': fields.String(max_length=64),
    'group_id': fields.String(max_length=36),
})

Hours = Model('Hours', {
    'twentyfourseven': fields.Boolean(required=True, description='True to represent 24 hours a day and 7 days a week, except the given exceptions.'),
    'regular_hours': fields.List(fields.Nested(RegularHours), description='Regular hours, weekday-based. Only to be used if twentyfourseven=false, then this field needs to contain at least one RegularHours object.'),
    'exceptional_openings': fields.List(fields.Nested(ExceptionalPeriod), description='Regular hours, weekday-based. Only to be used if twentyfourseven=false, then this field needs to contain at least one RegularHours object.'),
    'exceptional_closings': fields.List(fields.Nested(ExceptionalPeriod), description='Regular hours, weekday-based. Only to be used if twentyfourseven=false, then this field needs to contain at least one RegularHours object.'),
})

StatusSchedule = Model('StatusSchedule', {
    'period_begin': fields.DateTime(required=True, description='Begin of the scheduled period.'),
    'period_end': fields.DateTime(description='End of the scheduled period, if known.'),
    'status': fields.String(enum=status, required=True, description='Status value during the scheduled period.'),
})

Connector = Model('Connector', {
    'id':     fields.String(max_length=36, required=True, description='Identifier of the Connector within the EVSE. Two Connectors may have the same id as long as they do not belong to the same EVSE object.'),
    'standard':  fields.String(enum=connector_type, required=True, description='The standard of the installed connector.'),
    'format':    fields.String(enum=connector_format, required=True, description='The format (socket/cable) of the installed connector.'),
    'power_type': fields.String(enum=power_type, required=True, description='Type of power outlet'),
    'max_voltage':  fields.Integer(required=True, description='Maximum voltage of the connector (line to neutral for AC_3_PHASE), in volt [V]. For example: DC Chargers might vary the voltage during charging when battery almost full.'),
    'max_amperage': fields.Integer(required=True, description='Maximum amperage of the connector, in ampere [A].'),
    'max_electric_power': fields.Integer(description='Maximum electric power that can be delivered by this connector, in Watts (W). When the maximum electric power is lower than the calculated value from voltage and amperage, this value should be set.'),
    'tariff_ids':  fields.List(fields.String(max_length=36, required=True, description='Identifiers of the currently valid charging tariffs. Multiple tariffs are possible, but only one of each Tariff.type can be active at the same time.')),
    'terms_and_conditions': fields.String(description='URL to the operator’s terms and conditions.'),
    'last_updated': fields.DateTime(required=True, description='Timestamp when this Connector was last updated (or created).'),

})

EVSE = Model('EVSE', {
    'uid':     fields.String(max_length=36, required=True, description='Uniquely identifies the EVSE within the CPOs platform (and suboperator platforms). For example a database ID or the actual "EVSE ID". This field can never be changed, modified or renamed.'),
    'evse_id':     fields.String(max_length=48, description='Compliant with the following specification for EVSE ID from "eMI3 standard version V1.0"'),
    'status':      fields.String(enum=status, required=True, description='Indicates the current status of the EVSE.'),
    'status_schedule': fields.List(fields.Nested(StatusSchedule), description='Indicates a planned status update of the EVSE.'),
    'capabilities': fields.List(fields.String(enum=capability), description='List of functionalities that the EVSE is capable of.'),
    'connectors':   fields.List(fields.Nested(Connector), description='List of available connectors on the EVSE.'),
    'floor_level':  fields.String(max_length=4, description='Level on which the Charge Point is located (in garage buildings) in the locally displayed numbering scheme.'),
    'coordinates':  fields.Nested(GeoLocation, max_length=255, description='Coordinates of the EVSE.'),
    'physical_reference':  fields.String(max_length=16, description='A number/string printed on the outside of the EVSE for visual identification.'),
    'directions':   fields.List(fields.Nested(DisplayText), description='Multi-language human-readable directions when more detailed information on how to reach the EVSE from the Location is required.'),
    'parking_restrictions': fields.List(fields.String(enum=parking_restrictions), description='The restrictions that apply to the parking spot.'),
    'images':       fields.List(fields.Nested(Image), description='Links to images related to the EVSE such as photos or logos.'),
    'last_updated': fields.DateTime(required=True, description='Timestamp when this EVSE or one of its Connectors were last updated (or created).')
})

Location = Model('Location', {
    'country_code': CaseInsensitiveString(max_length=2, required=True, description="ISO-3166 alpha-2 country code of the CPO that 'owns' this Location."),
    'party_id':     CaseInsensitiveString(max_length=3, required=True, description="CPO ID of the CPO that 'owns' this Location (following the ISO-15118 standard)."),
    'id':           CaseInsensitiveString(max_length=36, required=True, description='Uniquely identifies the location within the CPOs platform (and suboperator platforms). This field can never be changed, modified or renamed.'),
    'publish':      fields.Boolean(required=True, default=True, description='Defines if a Location may be published on an website or app etc.'),
    'publish_allowed_to': fields.List(fields.String(description='Only owners of Tokens that match all the set fields of one PublishToken in the list are allowed to be shown this location.')),
    'name':         fields.String(max_length=255, description='Display name of the location.'),
    'address':      fields.String(max_length=45, required=True, description='Street/block name and house number if available.'),
    'city':         fields.String(max_length=45, required=True, description='City or town.'),
    'postal_code':  fields.String(max_length=10, description='Postal code of the location, may only be omitted when the location has no postal code: in some countries charging locations at highways don’t have postal codes.'),
    'state':        fields.String(max_length=20, required=True, description='State or province of the location, only to be used when relevant.'),
    'country':      fields.String(max_length=3, required=True, description='ISO 3166-1 alpha-3 code for the country of this location.'),
    'coordinates':  fields.Nested(GeoLocation, required=True, description='Coordinates of the location.'),
    'related_locations': fields.List(fields.Nested(AdditionalGeoLocation), description='Geographical location of related points relevant to the user.'),
    'parking_type': fields.String(enum=parking_type, description='The general type of parking at the charge point location.'),
    'evses':        fields.List(fields.Nested(EVSE), description='List of EVSEs that belong to this Location.'),
    'directions':   fields.Float(description='Human-readable directions on how to reach the location.'),
    'operator':     fields.Nested(BusinessDetails, description='Information of the operator. When not specified, the information retrieved from the Credentials module should be used instead.'),
    'suboperator':  fields.Nested(BusinessDetails, description='Information of the suboperator if available.'),
    'owner':        fields.Nested(BusinessDetails, description='Information of the owner if available.'),
    'facilities':   fields.List(fields.String(description='Optional list of facilities this charging location directly belongs to.')),
    'time_zone':    fields.String(required=True, description='One of IANA tzdata’s TZ-values representing the time zone of the location.'),
    'opening_times': fields.Nested(Hours, description='The times when the EVSEs at the location can be accessed for charging.'),
    'charging_when_closed': fields.Boolean(default=True, description='Indicates if the EVSEs are still charging outside the opening hours of the location.'),
    'images':       fields.List(fields.Nested(Image), description='Links to images related to the location such as photos or logos.'),
    'energy_mix':   fields.Nested(EnergyMix, description='Details on the energy supplied at this location.'),
    'last_updated': fields.DateTime(required=True, description='Timestamp when this Location or one of its EVSEs or Connectors were last updated (or created).')
})


def add_models_to_location_namespace(namespace):
    for model in [Location, EVSE, Connector, StatusSchedule, PublishTokenType,
                  RegularHours, ExceptionalPeriod, Image, EnergyMix, EnergySource,
                  EnvironmentalImpact, AdditionalGeoLocation, BusinessDetails, GeoLocation,
                  RegularHours, ExceptionalPeriod, PublishTokenType, Hours,
                  DisplayText]:
        namespace.models[model.name] = model