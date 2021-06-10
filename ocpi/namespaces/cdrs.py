"""
Created on Wed June 09 2021
https://github.com/ocpi/ocpi/blob/master/mod_cdrs.asciidoc
@author: gruell
"""
#TODO: check receiver and sender interface

import logging
from flask_restx import Resource, Namespace
from ocpi.models import resp, respList
from ocpi.decorators import get_header_parser, token_required, pagination_parser
from ocpi.models.cdrs import add_models_to_cdr_namespace, Cdr
from datetime import datetime

cdrs_ns = Namespace(name="cdrs", validate=True)

add_models_to_cdr_namespace(cdrs_ns)
parser = get_header_parser(cdrs_ns)

log = logging.getLogger('ocpi')

def receiver():
    @cdrs_ns.route('/<string:cdr_uid>')
    @cdrs_ns.expect(parser)
    class manage_cdrs(Resource):
        def __init__(self, api=None, *args, **kwargs):
            self.cdrmanager = kwargs['cdrs']
            super().__init__(api, *args, **kwargs)

        @cdrs_ns.marshal_with(resp(cdrs_ns, Cdr))
        @token_required
        def get(self, cdr_uid):
            '''
            Retrieve an existing CDR.
            '''
            data = self.cdrmanager.getCdr(cdr_uid)
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

        @cdrs_ns.expect(Cdr)
        @token_required
        def post(self):
            '''
            Send a new CDR.
            '''
            data = self.cdrmanager.postCdr(cdrs_ns.payload)
            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }


def sender():
    @cdrs_ns.route('/', doc={"description": "API Endpoint for CDRs management"})
    @cdrs_ns.expect(parser)
    class get_cdrs(Resource):

        def __init__(self, api=None, *args, **kwargs):
            self.cdrmanager = kwargs['cdrs']
            super().__init__(api, *args, **kwargs)

        @cdrs_ns.doc(params={
            'date_from': {'in': 'query', 'description': 'Only return CDRs that have last_updated after or equal to this Date/Time (inclusive).',
                     'default': '2021-01-01T13:30:00+02:00', 'required': True},
            'date_to': {'in': 'query', 'description': 'Only return CDRs that have last_updated up to this Date/Time, but not including (exclusive).', 'default': '2038-01-01T15:30:00+02:00',
                   'required': True},
            'offset': {'in': 'query', 'description': 'The offset of the first object returned. Default is 0.', 'default': '0'},
            'limit': {'in': 'query', 'description': 'Maximum number of objects to GET.', 'default': '50'},
        })
        @cdrs_ns.marshal_with(respList(cdrs_ns, Cdr))
        @token_required
        def get(self):
            '''
            Fetch CDRs last updated (which in the current version of OCPI can only be the creation Date/Time) between the {date_from} and {date_to} (paginated).
            '''
            parser = pagination_parser()
            args = parser.parse_args()

            data = self.cdrmanager.getCdrs(args['from'], args['to'], args['offset'], args['limit'])

            return {'data': data,
                    'status_code': 1000,
                    'status_message': 'nothing',
                    'timestamp': datetime.now()
                    }

def makeCdrNamespace(interfaces=['SENDER', 'RECEIVER']):
    if 'SENDER' in interfaces:
        sender()
    if 'RECEIVER' in interfaces:
        receiver()
    return cdrs_ns