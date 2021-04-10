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


class SessionManager(object):

    def __init__(self):
        self.sessions = {}
        self.charging_prefs = {}

    def getSessions(self, begin, end, offset, limit):
        return list(self.sessions.values())[offset:offset+limit]

    def getSession(self, session_id):
        ses = self.sessions.get(session_id)
        if not ses:
            raise NotFound('session does not exist')
        return ses

    def createSession(self, session):
        self.sessions[session['session_id']] = session
        return 204

    def patchSession(self, session_id, sessionPart):
        ses = self.sessions.get(session_id)
        if not ses:
            raise NotFound('session does not exist')
        return ses.update(sessionPart)

    def updateChargingPrefs(self, session_id, prefs):
        #ses = self.sessions.get(session_id)
        # if 'CHARGING_PROFILE_CAPABLE' in evse[ses['evse_uid']]['capabilities']:
        # check if evse is capable of charging prefs

        self.charging_prefs[session_id] = prefs
        return {'ACCEPTED'}


class CredentialsManager(object):

    def __init__(self, credentials_role: mc.CredentialsRole, url):
        self.credentials = {}
        self.credentials_role = credentials_role
        self.url = url

    def createCredentials(self) -> mc.Credentials:
        token = secrets.token_urlsafe(32)  # tokenB
        c = {
            "token": token,
            "url": self.url,
            "roles": [self.credentials_role]
        }

        # Valid comm token, no token to access client
        self.credentials[token] = ''
        return c

    def makeRegistration(self, payload: mc.Credentials):
        # for initial handshake
        key = request.headers['Authorization']
        self.unregister(key)
        newCredentials = self.createCredentials()  # tokenC
        self.credentials[newCredentials['token']] = payload

        # TODO fetch endpoints from payload['url']
        return newCredentials

    def versionUpdate(self, payload: mc.Credentials):
        # TODO fetch endpoints from payload['url']
        return self.makeRegistration(payload)

    def unregister(self, token):
        try:
            self.credentials.pop(token)
            # token to access the other system is still valid.
        except:
            return 'method not allowed', 405
        return '', 200

    def isAuthenticated(self, token):
        return token in self.credentials.keys()


class LocationManager(object):
    def __init__(self):
        self.locations = {}

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