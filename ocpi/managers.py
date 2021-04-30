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

log = logging.getLogger('ocpi')
# sender interface


class ReservationManager():

    def __init__(self):
        self.reservations = {}

    def getReservations(self, begin, end, offset, limit):
        return list(self.reservations.values())[offset:offset+limit]

    def getReservation(self, country_id, party_id, reservation_id):
        log.debug('got reservation')
        return 204

    def addReservation(self, country_id, party_id, reservation):
        log.debug('add reservation')
        return 204

    def updateReservation(self, country_id, party_id, reservation_id, reservationPart):
        log.debug('update reservation')
        pass

    def updateChargingPrefs(self, reservation_id, prefs):
        pass


class SessionManager():

    def __init__(self):
        self.sessions = {}

    def getSessions(self, begin, end, offset, limit):
        log.debug('get sessions')
        return list(self.sessions.values())[offset:offset+limit]

    def getSession(self, country_id, party_id, session_id):
        log.debug('get session')
        return 204

    def createSession(self, country_id, party_id, session):
        log.debug('create session')
        return 204

    def patchSession(self, country_id, party_id, session_id, sessionPart):
        log.debug('patch session')
        pass

    def updateChargingPrefs(self, session_id, prefs):
        pass


class ParkingSessionManager():

    def __init__(self):
        self.parkingSessions = {}

    def getParkingSessions(self, begin, end, offset, limit):
        log.debug('get parking sessions')
        return list(self.parkingSessions.values())[offset:offset+limit]

    def getParkingSession(self, country_id, party_id, ParkingSession_id):
        log.debug('get parking session')
        return 204

    def createParkingSession(self, country_id, party_id, ParkingSession):
        log.debug('create parking session')
        return 204

    def patchParkingSession(self, country_id, party_id, ParkingSession_id, ParkingSessionPart):
        pass


class CredentialsManagerStub():

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


class CredentialsManager():

    def __init__(self, credentials_role: mc.CredentialsRole, url):
        self.credentials_role = credentials_role
        self.url = url
        self.tokens={}

    def createCredentials(self) -> mc.Credentials:
        token = secrets.token_urlsafe(32)  # tokenB
        c = {
            "token": token,
            "url": self.url,
            "roles": [self.credentials_role]
        }
        self.tokens[token]=c
        # Valid comm token, no token to access client
        return c

    def makeRegistration(self, payload: mc.Credentials):
        # for initial handshake
        key = request.headers['Authorization']
        self.unregister(key)
        newCredentials = self.createCredentials()  # tokenC

        self.tokens[newCredentials['token']]={'client_url':payload['url'],'client_token':payload['token']}
        return newCredentials

    def versionUpdate(self, payload: mc.Credentials):
        return self.makeRegistration(payload)

    def unregister(self, token):
        res = self.tokens.pop(token, None)
        if res is None:
            return 'method not allowed', 405
        return '', 200

    def isAuthenticated(self, token):
        return token in self.tokens.keys()

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
        log.debug('start sessions')
        pass

    def stopSession(self, session_info):
        log.debug('stop sessions')
        pass

    def unlockConnector(self, session_info):
        log.debug('unlock connector')
        pass

    def cancelReservation(self, session_info):
        log.debug('cancel reservation')
        pass

    def reserveNow(self, session_info):
        log.debug('reserve now')
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