#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 12:47:48 2021

@author: maurer
"""
import requests
from multiprocessing import RLock
import json
import ocpi.models.credentials as mc
import logging
import secrets
import base64
import os


def createOcpiHeader(token):
    encToken = base64.b64encode(token.encode("utf-8")).decode('utf-8')
    return {
        'Authorization': 'Token '+encToken,
        'X-Request-ID': secrets.token_urlsafe(8)
    }


log = logging.getLogger('ocpi')
# sender interface


class ReservationManager():

    def __init__(self):
        self.reservations = {}

    def getReservations(self, begin, end, offset, limit):
        return list(self.reservations.values())[offset:offset+limit], {}

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
        return list(self.sessions.values())[offset:offset+limit], {}

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
        return list(self.parkingSessions.values())[offset:offset+limit], {}

    def getParkingSession(self, country_id, party_id, ParkingSession_id):
        log.debug('get parking session')
        return 204

    def createParkingSession(self, country_id, party_id, ParkingSession):
        log.debug('create parking session')
        return 204

    def patchParkingSession(self, country_id, party_id, ParkingSession_id, ParkingSessionPart):
        pass


class CredentialsManager():

    def __init__(self, credentials_roles: mc.CredentialsRole, url, **kwds):
        self.credentials_roles = credentials_roles
        self.url = url
        super().__init__(**kwds)

    def _getEndpoints(self, client_url, client_version='2.2'):
        endpoints = []
        try:
            response = requests.get(f'{client_url}/{client_version}')

            endpoints = response.json()['data']['endpoints']
        except requests.exceptions.ConnectionError:
            log.error(f"no version details, connection to {client_url} failed")
        except Exception:
            log.exception(
                f'could not get version details from {client_url}, {client_version}')
        return endpoints

    def _sendRegisterResponse(self, url, version, token, access_client):
        data = {"token": token,
                "url": self.url,
                "roles": self.credentials_roles}
        header = createOcpiHeader(access_client)
        resp = requests.post(
            f'{url}/{version}/credentials', json=data, headers=header)
        if resp.status_code == 405:
            resp = requests.put(
                f'{url}/{version}/credentials', json=data, headers=header)
        resp.raise_for_status()
        # catch as requests.exceptions.HTTPError
        # get e.response.status_code

        data = resp.json()
        log.info(f'registration successful: {data}')
        return data['data']['token']
        # TODO check roles and business details
        # data['data']['roles']

    def _pushObjects(self, objects, method, token, endpoint_url, with_path=True):
        headers = createOcpiHeader(token)
        for r in objects:
            try:
                if with_path:
                    url = f"{endpoint_url}/{r['country_code']}/{r['party_id']}/{r['id']}"
                else:
                    url = endpoint_url

                if method == 'PUT':
                    res = requests.put(url, headers=headers, json=r)
                elif method == 'PATCH':
                    res = requests.patch(url, headers=headers, json=r)
                elif method == 'POST':
                    res = requests.post(url, headers=headers, json=r)
                else:
                    raise Exception('invalid method provided: {method}')

                res.raise_for_status()
            except requests.exceptions.HTTPError as e:
                log.warning(f'ocpi {method} object {e.response.status_code} - {e.response.text} - {url}')
            except requests.exceptions.ConnectionError:
                log.warning(f'could not connect to {url}')
            except Exception:
                log.exception(f'error sending to {url}')

    def makeRegistration(self, payload: mc.Credentials, tokenA: str):
        # tokenA used to get here for initial handshake
        self._deleteToken(tokenA)
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

    def sendToModule(self, objects, module, method='PUT', with_path=True):
        raise NotImplementedError()

    def _updateToken(self, token, client_url, client_token, endpoint_list=None):
        raise NotImplementedError()

    def _deleteToken(self, token):
        raise NotImplementedError()

    def getCredentials(self, token: str) -> mc.Credentials:
        return {
            "token": token,  # this is plain text and not base64
            "url": self.url,
            "roles": [self.credentials_roles]
        }


class CredentialsDictMan(CredentialsManager):

    lock = RLock()

    def __init__(self, credentials_roles: mc.CredentialsRole, url, filename='ocpi_creds.json'):
        self.filename = filename
        with CredentialsDictMan.lock:
            if not os.path.isfile(filename):
                self.writeJson({})
        super().__init__(credentials_roles, url)

    def readJson(self):
        with CredentialsDictMan.lock:
            with open(self.filename, 'r') as f:
                return json.load(f)

    def writeJson(self, endpoints):
        with CredentialsDictMan.lock:
            with open(self.filename, 'w') as f:
                json.dump(endpoints, f, indent=4, sort_keys=False)

    def isAuthenticated(self, token):
        return token in self.readJson()

    def sendToModule(self, objects, module, method='PUT', with_path=True):
        for token in self.readJson().values():
            actual_module = list(filter(lambda t: t['identifier']==module,token['endpoints']))
            if actual_module:
                self._pushObjects(objects, method, token['client_token'], actual_module[0]['url'])

    def _updateToken(self, token, client_url, client_token, endpoint_list=None):
        data = {
            'client_url': client_url,
            'client_token': client_token,
            'endpoints': endpoint_list or []}
        with CredentialsDictMan.lock:
            tokens = self.readJson()
            tokens[token] = data
            self.writeJson(tokens)
        log.debug(f'current tokens: {tokens}')

    def _deleteToken(self, token):
        with CredentialsDictMan.lock:
            tokens = self.readJson()
            tokens.pop(token, None)
            self.writeJson(tokens)


class LocationManager(object):
    def __init__(self):
        self.locations = {}

    def getLocations(self, begin, end, offset, limit):
        return list(self.locations.values())[offset:offset+limit], {}

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

    def startSession(self, session_info, token):
        log.debug('start sessions')
        pass

    def stopSession(self, session_info, token):
        log.debug('stop sessions')
        pass

    def unlockConnector(self, session_info, token):
        log.debug('unlock connector')
        pass

    def cancelReservation(self, session_info, token):
        log.debug('cancel reservation')
        pass

    def reserveNow(self, session_info, token):
        log.debug('reserve now')
        pass

    def startSessionResult(self, session_info, token):
        log.debug('start sessions result')
        pass

    def stopSessionResult(self, session_info, token):
        log.debug('stop sessions result')
        pass

    def unlockConnectorResult(self, session_info, token):
        log.debug('unlock connector result')
        pass

    def cancelReservationResult(self, session_info, token):
        log.debug('cancel reservation result')
        pass

    def reserveNowResult(self, session_info, token):
        log.debug('reserve now result')
        pass


class VersionManager():
    def __init__(self, base_url, endpoints: dict, ocpi_version='2.2'):
        self._base_url = base_url
        self._ocpi_version = ocpi_version
        self._details = self._makeDetails(endpoints)

        # TODO support multiple Versions

    def _makeDetails(self, endpoints):
        res = []
        for ep_name, role in endpoints.items():
            e = {}
            e['identifier'] = ep_name
            e['role'] = role
            e['url'] = f'{self._base_url}/{self._ocpi_version}/{ep_name}'
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
        return list(self.tokens.values())[offset:offset+limit], {}

    def getToken(self, country_code, party_id, token_uid, type=None):
        return self.tokens[token_uid]

    def putToken(self, country_code, party_id, token_uid, token, type=None):
        self.tokens[token_uid] = token

    def patchToken(self, country_code, party_id, token_uid, token, type=None):
        self.tokens[token_uid].update(token)

    def validateToken(self, token_uid, type=None, location=None):
        # When the token is known by the Sender, the response SHALL contain a AuthorizationInfo object.
        if token_uid in self.tokensmanager.tokens.keys():
            data = None  # TODO: fill data with AuthorizationInfo here
            statuscode = 1000
            statusmessage = 'token found'
            return data, statuscode, statusmessage
        # If the token is not known, the response SHALL contain the status code: 2004: Unknown Token, and no data field.
        else:
            data = None
            statuscode = 2004
            statusmessage = 'Unknown Token'
            return data, statuscode, statusmessage


class TariffsManager(object):
    def __init__(self):
        self.tariffs = {}

    def getTariffs(self, begin, end, offset, limit):
        return list(self.tariffs.values())[offset:offset+limit], {}

    def getTariff(self, country_code, party_id, tariff_id):
        return self.tariffs[tariff_id]

    def putTariff(self, country_code, party_id, tariff_id, tariff):
        self.tariffs[tariff_id] = tariff
        return 'accepted'

    def deleteTariff(self, country_code, party_id, tariff_id):
        del self.tariffs[tariff_id]


class ChargingProfilesManager(object):
    def __init__(self):
        self.ChargingProfiles = {}

    # Retrieves the ActiveChargingProfile as it is currently planned for the the given session.
    def getChargingProfile(self, session_id, duration, response_url):
        # return type: ChargingProfileResponse
        pass

    # Creates a new ChargingProfile on a session, or replaces an existing ChargingProfile on the EVSE.
    def putChargingProfile(self, session_id, set_charging_profile):
        self.ChargingProfiles[session_id] = set_charging_profile['charging_profile']
        # return type: ChargingProfileResponse
        pass

    def handleActiveChargingProfileResult(self, session_id, charging_profile):
        pass

    def handleChargingProfileResult(self, session_id, charging_profile):
        pass

    def handleClearProfileResult(self, session_id, charging_profile):
        pass

    # Clears the ChargingProfile set by the eMSP on the given session.
    def deleteChargingProfile(self, session_id, response_url):
        # return type: ChargingProfileResponse
        pass

    def handleUpdateActiveChargingProfile(self, session_id, active_charging_profile):
        pass


class CdrManager(object):
    def __init__(self):
        self.cdrs = {}

    def getCdrs(self, begin, end, offset, limit):
        return list(self.cdrs.values())[offset:offset+limit], {}

    def getCdr(self, cdr_uid):
        return self.cdrs[cdr_uid]

    def postCdr(self, cdr):
        self.cdrs.append(cdr)
        # TODO: The response should contain the URL to the newly created CDR in the eMSP’s system, can be used by the CPO system to perform a GET on the same CDR.
        return self.cdrs[-1]
