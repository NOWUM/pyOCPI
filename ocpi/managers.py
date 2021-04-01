#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 12:47:48 2021

@author: maurer
"""


from flask import request
from werkzeug.exceptions import Forbidden, NotFound


class SessionManager(object):

    def __init__(self):
        self.sessions = {}
        self.charging_prefs = {}

    def getSessions(self,begin, end, offset,limit):
        return list(self.sessions.values())[offset:offset+limit]

    def getSession(self,session_id):
        ses= self.sessions.get(session_id)
        if not ses:
            raise NotFound('session does not exist')
        return ses

    def createSession(self, session):
        self.sessions[session['session_id']]=session
        return 204

    def patchSession(self, session_id,sessionPart):
        ses = self.sessions.get(session_id)
        if not ses:
            raise NotFound('session does not exist')
        return ses.update(sessionPart)

    def updateChargingPrefs(self, session_id, prefs):
        #ses = self.sessions.get(session_id)
        #if 'CHARGING_PROFILE_CAPABLE' in evse[ses['evse_uid']]['capabilities']:
        # check if evse is capable of charging prefs

        self.charging_prefs[session_id]=prefs
        return {'ACCEPTED'}


class ReservationManager(object):

    def __init__(self):
        self.reservations = []

    def create(self, payload):
        self.reservations.append(payload)
        return payload['price']*1.19+3


class CredentialsManager(object):

    def __init__(self):
        self.credentials = {}

    def createCredentials(self):
        c = {
            "token": "random_id",
            "url": "http://localhost:5000",
            "roles": []
        }

        self.credentials[c['token']] = c
        return c

    def updateRegistration(self, payload):
        c = {
            "token": "random_id",
            "url": "http://localhost:5000",
            "roles": []
        }

        self.credentials[c['token']] = c
        return c

    def replaceToken(self, payload):
        self.removeToken(payload)

        return self.createCredentials()

    def removeToken(self, payload):
        try:
            if request.headers['Authorization'] != payload['token']:
                raise Forbidden
            self.credentials.pop(payload['token'])
        except:
            return 405, 'method not allowed'
        return 200


cm = CredentialsManager()


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