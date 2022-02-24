#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 15:03:13 2021

@author: maurer
"""

from flask_restx import fields
from .sessions import BaseSession, add_models_to_session_namespace
from .tariffs import PriceComponent


parking_status = [
    "REQUEST",
    "ACTIVE",
    "COMPLETED",
    "INVALID",
    "PENDING",
    "RESERVATION",
]

ParkingSession = BaseSession.clone("ParkingSession", {
    "license_plate": fields.String(description="License plate to identify parking session"),
    "status": fields.String(enum=parking_status, default="REQUEST", description="The status of the reservation."),
    "price_components": fields.List(
        fields.Nested(PriceComponent), description="List of Price Component elements needed to calculate the parking price"),
    'connect_date_time' : fields.DateTime(required=False, description='The timestamp when the session was connected to the CS. Can be omitted if same as start_date_time'),
    'disconnect_date_time' : fields.DateTime(required=False, description='The timestamp when the session was disconnected from the CS. Can be omitted if same as end_date_time'),
})


def add_models_to_parking_namespace(namespace):
    for model in [ParkingSession, PriceComponent]:
        namespace.models[model.name] = model
    add_models_to_session_namespace(namespace)