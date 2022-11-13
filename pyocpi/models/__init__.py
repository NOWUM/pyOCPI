#

from flask_restx import fields


def respRaw(namespace, model):
    return namespace.model(model.name+'Response', {
        'data': model,
        'status_code': fields.Integer(required=True),
        'status_message': fields.String(),
        'timestamp': fields.DateTime(required=True),
    })


def resp(namespace, model):
    '''
    create ocpi response model
    https://github.com/ocpi/ocpi/blob/master/transport_and_format.asciidoc#116-response-format
    '''
    return namespace.model(model.name+'Response', {
        'data': fields.Nested(model),
        'status_code': fields.Integer(required=True),
        'status_message': fields.String(),
        'timestamp': fields.DateTime(required=True),
    })


def respList(namespace, model):
    '''
    create ocpi response model
    https://github.com/ocpi/ocpi/blob/master/transport_and_format.asciidoc#116-response-format
    '''
    return namespace.model(model.name+'Response', {
        'data': fields.List(fields.Nested(model)),
        'status_code': fields.Integer(required=True),
        'status_message': fields.String(),
        'timestamp': fields.DateTime(required=True),
    })