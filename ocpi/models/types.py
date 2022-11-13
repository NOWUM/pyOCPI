#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 22:24:19 2021

@author: maurer
"""

from flask_restx import fields, Model


class CaseInsensitiveString(fields.String):
    def format(self, value):
        return super().format(value.upper())


DisplayText = Model('DisplayText', {
    'language': fields.String(max_length=2, required=True, description='Language Code ISO 639-1.'),
    'text': fields.String(max_length=512, required=True, description='Text to be displayed to a end user. No markup, html etc. allowed.'),
})

role = [
    'CPO'	,  # Charge Point Operator Role.
    'EMSP'	,  # eMobility Service Provider Role.
    'HUB'	,  # Hub role.
    # National Access Point Role (national Database with all Location information of a country).
    'NAP'	,
    # Navigation Service Provider Role, role like an eMSP (probably only interested in Location information).
    'NSP'	,
    'OTHER'	,  # Other role.
    'SCSP'	,  # Smart Charging Service Provider Role.
]