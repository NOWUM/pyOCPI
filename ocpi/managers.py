#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 12:47:48 2021

@author: maurer
"""
import requests
from multiprocessing import Lock
import json
import ocpi.models.credentials as mc
import logging
import base64
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

    def _getEndpoints(self,client_url):
        try:
            response = requests.get(client_url+'/versions/details')

            endpoints = response.json()['data']['endpoints']
        except:
            endpoints = []
            log.exception(f'could not get version details from {client_url}')
        return endpoints

    def _sendRegisterResponse(self, url, version, token, access_client):
        data = {"token": token,
                "url": self.url,
                "roles": self.credentials_roles}
        encToken = base64.b64encode(
            access_client.encode("utf-8")).decode('utf-8')
        resp = requests.post(f'{url}/{version}/credentials', json=data, headers={
            'Authorization': 'Token '+encToken,
            'X-Request-ID': secrets.token_urlsafe(8)})
        if resp.status_code == 200:

            data = resp.json()
            log.info(f'registration successfull: {data}')
            return data['data']['token']
            # TODO check roles and business details
            # data['data']['roles']
        else:
            raise Exception(f'{url} - HTTP {resp.status_code} - {resp.text}')

    def makeRegistration(self, payload: mc.Credentials, tokenA: str):
        # tokenA used to get here for initial handshake
        self.unregister(tokenA)
        tokenB = payload['token']
        client_url = payload['url']

        tokenC = secrets.token_urlsafe(32)  # plain
        newCredentials = {
            "token": tokenC,  # this is plain text and not base64
            "url": self.url,
            "roles": self.credentials_roles
        }
        endpoints = self._getEndpoints(client_url)
        self._updateToken(tokenC, client_url, tokenB, endpoints)
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

    def _updateToken(self, token, client_url, client_token, endpoint_list=[]):
        raise NotImplementedError()

    def _deleteToken(self, token):
        raise NotImplementedError()

    def getCredentials(self, token: str) -> mc.Credentials:
        return {
            "token": token,  # this is plain text and not base64
            "url": self.url,
            "roles": [self.credentials_roles]
        }


lock = Lock()


class CredentialsDictMan(CredentialsManager):
    def __init__(self, credentials_roles: mc.CredentialsRole, url, filename='ocpi_creds.json'):
        self.filename = filename
        with lock:
            self.writeJson({})
        super().__init__(credentials_roles, url)

    def readJson(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def writeJson(self, endpoints):
        with open(self.filename, 'w') as f:
            json.dump(endpoints, f, indent=4, sort_keys=False)

    def isAuthenticated(self, token):
        return token in self.readJson()

    def _updateToken(self, token, client_url, client_token, endpoint_list=[]):
        data = {
            'client_url': client_url,
            'client_token': client_token,
            'endpoints': endpoint_list}
        with lock:
            tokens = self.readJson()
            tokens[token] = data
            self.writeJson(tokens)
        log.info(f'current tokens: {tokens}')

    def _deleteToken(self, token):
        with lock:
            tokens = self.readJson()
            tokens.pop(token, None)
            self.writeJson(tokens)


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

class TokensManager(object):
    def __init__(self):
        self.tokens = {}

    def getTokens(self, begin, end, offset, limit):
        return list(self.tokens.values())[offset:offset+limit]

    def getToken(self, country_code, party_id, token_uid, type=None):
        return self.tokens[token_uid]

    def putToken(self, country_code, party_id, token_uid, token, type=None):
        self.tokens[token_uid] = token

    def patchToken(self, country_code, party_id, token_uid, token, type=None):
        self.tokens[token_uid].update(token)