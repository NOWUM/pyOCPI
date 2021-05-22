#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 15:03:13 2021

@author: maurer
"""

from .sessions import BaseSession, add_models_to_session_namespace
from .tariffs import TariffElement, TariffRestrictions, PriceComponent
from flask_restx import fields
parking_status = ["REQUEST", "ACTIVE",
                  "COMPLETED", "INVALID", "PENDING", "RESERVATION"]

ParkingSession = BaseSession.clone("ParkingSession", {
    'license_plate': fields.String(description='License plate to identify parking session'),
    'currency': fields.String(max_length=3, description='ISO 4217 code of the currency used for this session.'),
    'status': fields.String(enum=parking_status, default="REQUEST", description='The status of the reservation.'),
    'total_cost': fields.Float(description='The total cost of the parking_session in the specified currency. This is the price that the eMSP will have to pay to the PSO.'),
    'tariff_elements': fields.List(fields.Nested(TariffElement), description='List of Tariff elements needed to calculate the parking price')
})


def add_models_to_parking_namespace(namespace):
    for model in [ParkingSession, TariffElement, TariffRestrictions, PriceComponent]:
        namespace.models[model.name] = model
    add_models_to_session_namespace(namespace)