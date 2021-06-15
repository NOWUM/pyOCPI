"""
Created on Thu June 02 2021
https://github.com/ocpi/ocpi/blob/master/mod_tariffs.asciidoc
@author: gruell
"""
import logging
from flask_restx import Resource, Namespace
from ocpi.models import resp, respList
from ocpi.decorators import (get_header_parser, token_required,
                             pagination_parser, makeResponse)
from ocpi.models.tariffs import add_models_to_tariffs_namespace, Tariff
from datetime import datetime

tariffs_ns = Namespace(name="tariffs", validate=True)

add_models_to_tariffs_namespace(tariffs_ns)
parser = get_header_parser(tariffs_ns)

log = logging.getLogger('ocpi')

# (https://github.com/ocpi/ocpi/blob/master/mod_tariffs.asciidoc#122-receiver-interface)


def receiver():
    @tariffs_ns.route('/<string:country_code>/<string:party_id>/<string:tariff_id>')
    @tariffs_ns.expect(parser)
    class manage_tariffs(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.tariffsmanager = kwargs['tariffs']
            super().__init__(api, *args, **kwargs)

        @tariffs_ns.marshal_with(resp(tariffs_ns, Tariff))
        @token_required
        def get(self, country_code, party_id, tariff_id):
            '''
            Retrieve a Tariff as it is stored in the eMSP’s system.
            '''
            data = self.tariffsmanager.getTariff(
                country_code, party_id, tariff_id)
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        @tariffs_ns.expect(Tariff)  # Model for New or updated Tariff object.
        @tariffs_ns.marshal_with(resp(tariffs_ns, Tariff))
        @token_required
        def put(self, country_code, party_id, tariff_id):
            '''
            Push new/updated Tariff object to the eMSP.
            '''
            self.tariffsmanager.putTariff(
                country_code, party_id, tariff_id, tariffs_ns.payload)
            data = 'accepted'
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        @tariffs_ns.marshal_with(resp(tariffs_ns, Tariff))
        @token_required
        def delete(self, country_code, party_id, tariff_id):
            '''
            Remove a Tariff object which is no longer in use and will not be used in future either.
            '''
            self.tariffsmanager.deleteTariff(country_code, party_id, tariff_id)
            data = 'accepted'
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

# (https://github.com/ocpi/ocpi/blob/master/mod_tariffs.asciidoc#121-sender-interface)


def sender():
    @tariffs_ns.route('/', doc={"description": "API Endpoint for Tariffs management"})
    @tariffs_ns.expect(parser)
    class get_tariffs(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.tariffsmanager = kwargs['tariffs']
            super().__init__(api, *args, **kwargs)

        @tariffs_ns.doc(params={
            'date_from': {'in': 'query', 'description': 'Only return Tariffs that have last_updated after or equal to this Date/Time (inclusive).',
                          'default': '2021-01-01T13:30:00+02:00', 'required': True},
            'date_to': {'in': 'query', 'description': 'Only return Tariffs that have last_updated up to this Date/Time, but not including (exclusive).', 'default': '2038-01-01T15:30:00+02:00',
                        'required': True},
            'offset': {'in': 'query', 'description': 'The offset of the first object returned. Default is 0.', 'default': '0'},
            'limit': {'in': 'query', 'description': 'Maximum number of objects to GET.', 'default': '50'},
        })
        @tariffs_ns.marshal_with(respList(tariffs_ns, Tariff))
        @token_required
        def get(self):
            '''
            Returns Tariff objects from the CPO, last updated between the {date_from} and {date_to} (paginated)
            '''
            parser = pagination_parser()
            args = parser.parse_args()

            data, headers = self.tariffsmanager.getTariffs(
                args['from'], args['to'], args['offset'], args['limit'])
            return makeResponse(data, headers=headers)


def makeTariffsNamespace(interfaces=['SENDER', 'RECEIVER']):
    log.debug('tariffs interfaces:'+str(interfaces))
    if 'SENDER' in interfaces:
        sender()
    if 'RECEIVER' in interfaces:
        receiver()
    if 'CPO' in interfaces:
        sender()

    return tariffs_ns