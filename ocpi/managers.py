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


class CredentialsManager():

    def __init__(self, credentials_roles: mc.CredentialsRole, url):
        self.credentials_roles = credentials_roles
        self.url = url

    def makeRegistration(self, payload: mc.Credentials, tokenA: str):
        # tokenA used to get here for initial handshake
        self.unregister(tokenA)
        tokenB = payload['token']
        client_url = payload['url']

        tokenC = secrets.token_urlsafe(32)  # plain
        newCredentials = {
            "token": 'Token '+tokenC,  # this is plain text and not base64
            "url": self.url,
            "roles": self.credentials_roles
        }
        self._updateToken(tokenC, client_url, tokenB)
        return newCredentials

    def versionUpdate(self, payload: mc.Credentials, token: str):
        return self.makeRegistration(payload, token)

    def unregister(self, token):
        res = self._deleteToken(token)
        if res is None:
            return 'method not allowed', 405
        return '', 200

    def isAuthenticated(self, token):
        raise NotImplementedError()

    def _updateToken(self, token, client_url, client_token):
        raise NotImplementedError()

    def _deleteToken(self, token):
        raise NotImplementedError()

    def getCredentials(self, token: str) -> mc.Credentials:
        return {
            "token": 'Token '+token,  # this is plain text and not base64
            "url": self.url,
            "roles": [self.credentials_roles]
        }


class CredentialsDictMan(CredentialsManager):
    def __init__(self, credentials_roles: mc.CredentialsRole, url):
        self.tokens = {}
        super().__init__(credentials_roles, url)

    def isAuthenticated(self, token):
        return token in self.tokens

    def _updateToken(self, token, client_url, client_token):
        log.info(f'current tokens: {self.tokens}')
        data = {
            'client_url': client_url, 'client_token': client_token}
        self.tokens[token] = data

    def _deleteToken(self, token):
        return self.tokens.pop(token, None)


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
    def __init__(self, base_url, endpoints: list, roles=['SENDER'], ocpi_version='2.2'):
        self._base_url = base_url
        self._roles = roles
        self._ocpi_version = ocpi_version
        self._details = self._makeDetails(endpoints)

        # TODO support multiple Versions

    def _makeDetails(self, endpoints):
        res = []
        for role in self._roles:
            for key in endpoints:
                e = {}
                e['identifier'] = key
                e['role'] = role
                e['url'] = f'{self._base_url}/{self._ocpi_version}/{key}'
                res.append(e)
            return res

    def versions(self):
        return{
            'versions':
                [
                    {'version': self._ocpi_version,
                        'url': self._base_url+'/'+self._ocpi_version}
                ]
        }

    def details(self):
        return {
            'version': self._ocpi_version,
            'endpoints': self._details
        }