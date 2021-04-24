#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 12:47:48 2021

@author: maurer
"""


import ocpi.models.credentials as mc
from flask import request
from werkzeug.exceptions import Forbidden, NotFound
import logging
import secrets

# sender interface


class ReservationManager():

    def __init__(self):
        self.reservations = {}

    def getReservations(self, begin, end, offset, limit):
        return list(self.reservations.values())[offset:offset+limit]

    def getReservation(self, country_id, party_id, reservation_id):
        return 204

    def addReservation(self, country_id, party_id, reservation):
        return 204

    def updateReservation(self, country_id, party_id, reservation_id, reservationPart):
        pass

    def updateChargingPrefs(self, reservation_id, prefs):
        pass


class SessionManager():

    def __init__(self):
        self.sessions = {}

    def getSessions(self, begin, end, offset, limit):
        return list(self.sessions.values())[offset:offset+limit]

    def getSession(self, country_id, party_id, session_id):
        return 204

    def createSession(self, country_id, party_id, session):
        return 204

    def patchSession(self, country_id, party_id, session_id, sessionPart):
        pass

    def updateChargingPrefs(self, session_id, prefs):
        pass


class CredentialsManager():

    def __init__(self, credentials_role: mc.CredentialsRole, url):
        self.credentials_role = credentials_role
        self.url = url

    def createCredentials(self) -> mc.Credentials:
        pass

    def makeRegistration(self, payload: mc.Credentials):
        pass

    def versionUpdate(self, payload: mc.Credentials):
        return self.makeRegistration(payload)

    def unregister(self, token):
        pass

    def isAuthenticated(self, token):
        return True


class LocationManager(object):
    def __init__(self):
        self.locations = {}

    def getLocations(self, begin, end, offset, limit):
        return list(self.locations.values())[offset:offset+limit]

    def getLocation(self, country_id, party_id, location_id):
        return self.locations[location_id]

    def putLocation(self, country_id, party_id, location_id, location):
        self.locations[location_id] = location

    def patchLocation(self, country_id, party_id, location_id, location):
        self.locations[location_id].update(location)

    def getEVSE(self, country_id, party_id, location_id, evse_id):
        return self.locations[location_id]

    def putEVSE(self, country_id, party_id, location_id, evse_id, evse):
        self.locations[location_id][evse_id] = evse

    def patchEVSE(self, country_id, party_id, location_id, evse_id, evse):
        self.locations[location_id][evse_id].update(evse)

    def getConnector(self, country_id, party_id, location_id, evse_id, connector_id):
        return self.locations[location_id][evse_id][connector_id]

    def putConnector(self, country_id, party_id, location_id, evse_id, connector_id, connector):
        self.locations[location_id][evse_id][connector_id] = connector

    def patchConnector(self, country_id, party_id, location_id, evse_id, connector_id, connector):
        self.locations[location_id][evse_id][connector_id].update(connector)


class CommandsManager(object):
    def __init__(self):
        self.log = {}

    def startSession(self, session_info):
        pass

    def stopSession(self, session_info):
        pass

    def unlockConnector(self, session_info):
        pass

    def cancelReservation(self, session_info):
        pass

    def reserveNow(self, session_info):
        pass


class VersionManager():
    def __init__(self, base_url, endpoints: list, roles=['SENDER']):
        self.__base_url = base_url
        self.__roles = roles
        self.__details = self.__makeDetails(endpoints)

    def __makeDetails(self, endpoints):
        res = []
        for role in self.__roles:
            for key in endpoints:
                e = {}
                e['identifier'] = key
                e['role'] = role
                e['url'] = self.__base_url+'/'+key
                res.append(e)
            return res

    def versions(self):
        return{
            'versions':
                [
                    {'version': '2.2', 'url': self.__base_url}
                ]
        }

    def details(self):
        return {
            'version': '2.2',
            'endpoints': self.__details
        }