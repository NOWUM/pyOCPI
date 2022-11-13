"""
Created on Thu May 26 2021
https://github.com/ocpi/ocpi/blob/master/mod_tariffs.asciidoc
@author: maurer, gruell
"""

from flask_restx import Model, fields
from ocpi.models.types import DisplayText, CaseInsensitiveString
from ocpi.models.location import EnergyMix

# Enums:
tariff_dimension_type = ['ENERGY', 'FLAT',
                         'PARKING_TIME', 'TIME']  # TariffDimensionType
tariff_type = ['AD_HOC_PAYMENT', 'PROFILE_CHEAP',
               'PROFILE_FAST', 'PROFILE_GREEN', 'REGULAR']  # TariffType
day_of_week = ['MONDAY', 'TUESDAY', 'WEDNESDAY',
               'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']  # DayOfWeek
reservation_restriction_type = [
    'RESERVATION', 'RESERVATION_EXPIRES']  # ReservationRestrictionType

# Classes:

Price = Model('Price', {
    'excl_vat': fields.Float(required=True, description='Price/Cost excluding VAT.'),
    'incl_vat': fields.Float(description='Price/Cost including VAT.')
})

PriceComponent = Model('PriceComponent', {
    'type': fields.String(enum=tariff_dimension_type, required=True, description='Type of tariff dimension.'),
    'price': fields.Float(required=True, description='Price per unit (excl. VAT) for this tariff dimension.'),
    'vat': fields.Float(description='Applicable VAT percentage for this tariff dimension. If omitted, no VAT is applicable. Not providing a VAT is different from 0% VAT, which would be a value of 0.0 here.'),
    'step_size': fields.Integer(required=True, description='Minimum amount to be billed. This unit will be billed in this step_size blocks. Amounts that are less then this step_size are rounded up to the given step_size. For example: if type is TIME and step_size has a value of 300, then time will be billed in blocks of 5 minutes. If 6 minutes were used, 10 minutes (2 blocks of step_size) will be billed.'),
    'name': fields.String(description='Optional Extension to the OCPI protocol')
})

TariffRestrictions = Model('TariffRestrictions', {
    'start_time': fields.String(max_length=5, description='Start time of day in local time, the time zone is defined in the time_zone field of the Location, for example 13:30, valid from this time of the day. Must be in 24h format with leading zeros. Hour/Minute separator: ":" Regex: ([0-1][0-9]|2[0-3]):[0-5][0-9]'),
    'end_time': fields.String(max_length=5, description='End time of day in local time, the time zone is defined in the time_zone field of the Location, for example 19:45, valid until this time of the day. Same syntax as start_time. If end_time < start_time then the period wraps around to the next day. To stop at end of the day use: 00:00.'),
    'start_date': fields.String(max_length=10, description='Start date in local time, the time zone is defined in the time_zone field of the Location, for example: 2015-12-24, valid from this day (inclusive). Regex: ([12][0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])'),
    'end_date': fields.String(max_length=10, description='End date in local time, the time zone is defined in the time_zone field of the Location, for example: 2015-12-27, valid until this day (exclusive). Same syntax as start_date.'),
    'min_kwh': fields.Float(description='Minimum consumed energy in kWh, for example 20, valid from this amount of energy (inclusive) being used.'),
    'max_kwh': fields.Float(description='Maximum consumed energy in kWh, for example 50, valid until this amount of energy (exclusive) being used.'),
    'min_current': fields.Float(description='Sum of the minimum current (in Amperes) over all phases, for example 5. When the EV is charging with more than, or equal to, the defined amount of current, this TariffElement is/becomes active. If the charging current is or becomes lower, this TariffElement is not or no longer valid and becomes inactive. This describes NOT the minimum current over the entire Charging Session. This restriction can make a TariffElement become active when the charging current is above the defined value, but the TariffElement MUST no longer be active when the charging current drops below the defined value.'),
    'max_current': fields.Float(description='Sum of the maximum current (in Amperes) over all phases, for example 20. When the EV is charging with less than the defined amount of current, this TariffElement becomes/is active. If the charging current is or becomes higher, this TariffElement is not or no longer valid and becomes inactive. This describes NOT the maximum current over the entire Charging Session. This restriction can make a TariffElement become active when the charging current is below this value, but the TariffElement MUST no longer be active when the charging current raises above the defined value.'),
    'min_power': fields.Float(description='Minimum power in kW, for example 5. When the EV is charging with more than, or equal to, the defined amount of power, this TariffElement is/becomes active. If the charging power is or becomes lower, this TariffElement is not or no longer valid and becomes inactive. This describes NOT the minimum power over the entire Charging Session. This restriction can make a TariffElement become active when the charging power is above this value, but the TariffElement MUST no longer be active when the charging power drops below the defined value.'),
    'max_power': fields.Float(description='Maximum power in kW, for example 20. When the EV is charging with less than the defined amount of power, this TariffElement becomes/is active. If the charging power is or becomes higher, this TariffElement is not or no longer valid and becomes inactive. This describes NOT the maximum power over the entire Charging Session. This restriction can make a TariffElement become active when the charging power is below this value, but the TariffElement MUST no longer be active when the charging power raises above the defined value.'),
    'min_duration': fields.Integer(description='Minimum duration in seconds the Charging Session MUST last (inclusive). When the duration of a Charging Session is longer than the defined value, this TariffElement is or becomes active. Before that moment, this TariffElement is not yet active.'),
    'max_duration': fields.Integer(description='Maximum duration in seconds the Charging Session MUST last (exclusive). When the duration of a Charging Session is shorter than the defined value, this TariffElement is or becomes active. After that moment, this TariffElement is no longer active.'),
    'day_of_week': fields.List(fields.String(enum=day_of_week), description='Which day(s) of the week this TariffElement is active.'),
    'reservation': fields.String(enum=reservation_restriction_type, description='When this field is present, the TariffElement describes reservation costs. A reservation starts when the reservation is made, and ends when the driver starts charging on the reserved EVSE/Location, or when the reservation expires. A reservation can only have: FLAT and TIME TariffDimensions, where TIME is for the duration of the reservation.')
})

TariffElement = Model('TariffElement', {
    'price_components': fields.List(fields.Nested(PriceComponent), required=True, description='List of price components that describe the pricing of a tariff.'),
    'restrictions': fields.Nested(TariffRestrictions, description='Restrictions that describe the applicability of a tariff.')
})

# Objects:
Tariff = Model('Tariff', {
    'country_code': CaseInsensitiveString(max_length=2, required=True, description="ISO-3166 alpha-2 country code of the CPO that owns this Tariff."),
    'party_id': CaseInsensitiveString(max_length=3, required=True, description="CPO ID of the CPO that owns this Tariff (following the ISO-15118 standard)."),
    'id': CaseInsensitiveString(max_length=36, required=True, description='Uniquely identifies the tariff within the CPO’s platform (and suboperator platforms).'),
    'currency': fields.String(max_length=3, required=True, description='ISO-4217 code of the currency of this tariff.'),
    'type': fields.String(enum=tariff_type, required=False, description='Defines the type of the tariff. This allows for distinction in case of given Charging Preferences. When omitted, this tariff is valid for all sessions.'),
    'tariff_alt_text': fields.List(fields.Nested(DisplayText), required=False, description='List of multi-language alternative tariff info texts.'),
    'tariff_alt_url': fields.String(required=False, description='URL to a web page that contains an explanation of the tariff information in human readable form.'),
    'min_price': fields.Nested(Price, required=False, description='When this field is set, a Charging Session with this tariff will at least cost this amount. This is different from a FLAT fee (Start Tariff, Transaction Fee), as a FLAT fee is a fixed amount that has to be paid for any Charging Session. A minimum price indicates that when the cost of a Charging Session is lower than this amount, the cost of the Session will be equal to this amount. (Also see note below)'),
    'max_price': fields.Nested(Price, required=False, description='When this field is set, a Charging Session with this tariff will NOT cost more than this amount. (See note below)'),
    'elements': fields.List(fields.Nested(TariffElement), required=True, description='List of Tariff Elements.'),
    'start_date_time': fields.DateTime(required=False, description='The time when this tariff becomes active, in UTC, time_zone field of the Location can be used to convert to local time. Typically used for a new tariff that is already given with the location, before it becomes active. (See note below)'),
    'end_date_time': fields.DateTime(required=False, description='The time after which this tariff is no longer valid, in UTC, time_zone field if the Location can be used to convert to local time. Typically used when this tariff is going to be replaced with a different tariff in the near future. (See note below)'),
    'energy_mix': fields.Nested(EnergyMix, required=False, description='Details on the energy supplied with this tariff.'),
    'last_updated': fields.DateTime(required=True, description='Timestamp when this Token was last updated (or created).')
})


def add_models_to_tariffs_namespace(namespace):
    for model in [TariffElement, TariffRestrictions, Price, PriceComponent, Tariff]:
        namespace.models[model.name] = model