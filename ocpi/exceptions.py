#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: maurer
"""

class OcpiError(Exception):
    status_code = 3000

    def __init__(self, message=""):
        self.message = f'Generic Error {message}'


class InvalidMissingParamsError(OcpiError):
    status_code = 2001

    def __init__(self, message=""):
        self.message = f'Missing param {message}'

class NotEnoughInformationError(OcpiError):
    status_code = 2002
    message = 'Not enough information'

class InvalidLocationError(OcpiError):
    status_code = 2003
    message = 'Invalid Location'


class InvalidTokenError(OcpiError):
    status_code = 2004

    def __init__(self, message=""):
        self.message = f'Invalid Token {message}'

class ClientApiError(OcpiError):
    status_code = 2004

    def __init__(self, message=""):
        self.message = f'Unable to use the client’s API {message}'


class UnsupportedVersionError(OcpiError):
    status_code = 3002
    message = 'Unsupported Version'

    def __init__(self, message=""):
        if message:
            self.message = f'Unsupported Version {message}'