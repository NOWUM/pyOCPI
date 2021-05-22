# TODO: implement tariff models (https://github.com/ocpi/ocpi/blob/master/mod_tariffs.asciidoc)

from flask_restx import Model, fields


tarif_dimension_type = ['ENERGY', 'FLAT', 'PARKING_TIME', 'TIME']


PriceComponent = Model('PriceComponent', {
    'type': fields.String(enum=tarif_dimension_type, reqiored=True, description='Type of tariff dimension.'),
    'price': fields.Float(required=True, description='Price per unit (excl. VAT) for this tariff dimension.'),
    'vat': fields.Float(),
    'step_size': fields.Integer(required=True)
})

TariffRestrictions = Model('TariffRestrictions', {})

TariffElement = Model('TariffElement', {
    'price_components': fields.List(fields.Nested(PriceComponent), required=True),
    'restrictions': fields.Nested(TariffRestrictions),
})