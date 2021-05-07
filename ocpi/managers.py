#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 12:47:48 2021

@author: maurer
"""
import ocpi.models.credentials as mc
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


class CredentialPersistor():
    def __init__(self):
        self.tokens = {}

    def addToken(self, token, data):
        self.tokens[token] = data

    def updateToken(self, token, client_url, client_token):
        data = {
            'client_url': client_url, 'client_token': client_token}
        self.addToken(token, data)

    def deleteToken(self, token):
        return self.tokens.pop(token, None)

    def tokenExists(self, token):
        return token in self.tokens


class CredentialsManager():

    def __init__(self, credentials_role: mc.CredentialsRole, url, persistor):
        self.credentials_role = credentials_role
        self.url = url
        self.persistor = persistor

    def createCredentials(self, token: str) -> mc.Credentials:
        # TODO token a must have been used to get here
        # self.persistor.deleteToken(token)
        token = secrets.token_urlsafe(32)  # tokenB
        c = {
            "token": 'Token '+token,  # this is plain text and not base64
            "url": self.url,
            "roles": [self.credentials_role]
        }
        self.persistor.addToken(token, c)
        # Valid comm token, no token to access client
        return c

    def makeRegistration(self, payload: mc.Credentials, token: str):
        # for initial handshake
        self.unregister(token)
        newCredentials = self.createCredentials()  # tokenC
        newToken = newCredentials['token'].replace('Token ','') # this is always plain
        self.persistor.updateToken(newToken, payload['url'],payload['token'])
        return newCredentials

    def versionUpdate(self, payload: mc.Credentials, token: str):
        return self.makeRegistration(payload, token)

    def unregister(self, token):
        res = self.persistor.deleteToken(token)
        if res is None:
            return 'method not allowed', 405
        return '', 200

    def isAuthenticated(self, token):
        return self.persistor.tokenExists(token)


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