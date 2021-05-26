"""
Created on Thu May 26 2021
https://github.com/ocpi/ocpi/blob/master/mod_tariffs.asciidoc
@author: maurer, gruell
"""

from flask_restx import Model, fields


tariff_dimension_type = ['ENERGY', 'FLAT', 'PARKING_TIME', 'TIME']
tariff_type = ['AD_HOC_PAYMENT','PROFILE_CHEAP','PROFILE_FAST','PROFILE_GREEN','REGULAR'] #TariffType
day_of_week = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'] #DayOfWeek enum
reservation_restriction_type = ['RESERVATION', 'RESERVATION_EXPIRES']#ReservationRestrictionType enum


PriceComponent = Model('PriceComponent', {
    'type': fields.String(enum=tariff_dimension_type, reqiored=True, description='Type of tariff dimension.'),
    'price': fields.Float(required=True, description='Price per unit (excl. VAT) for this tariff dimension.'),
    'vat': fields.Float(description='Applicable VAT percentage for this tariff dimension. If omitted, no VAT is applicable. Not providing a VAT is different from 0% VAT, which would be a value of 0.0 here.'),
    'step_size': fields.Integer(required=True, description='Minimum amount to be billed. This unit will be billed in this step_size blocks. Amounts that are less then this step_size are rounded up to the given step_size. For example: if type is TIME and step_size has a value of 300, then time will be billed in blocks of 5 minutes. If 6 minutes were used, 10 minutes (2 blocks of step_size) will be billed.')
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
    'day_of_week': fields.List(fields.Nested(day_of_week),description='Which day(s) of the week this TariffElement is active.'),
    'reservation': fields.Nested(reservation_restriction_type, description='When this field is present, the TariffElement describes reservation costs. A reservation starts when the reservation is made, and ends when the driver starts charging on the reserved EVSE/Location, or when the reservation expires. A reservation can only have: FLAT and TIME TariffDimensions, where TIME is for the duration of the reservation.')

})

TariffElement = Model('TariffElement', {
    'price_components': fields.List(fields.Nested(PriceComponent), required=True, description='List of price components that describe the pricing of a tariff.'),
    'restrictions': fields.Nested(TariffRestrictions, description='Restrictions that describe the applicability of a tariff.')
})