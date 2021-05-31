#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib
from .UserResponse import UserResponse
from .TokenResponse import TokenResponse
from .ConnectionInfo import ConnectionInfo
from .ServerResponse import ServerResponse

api_url = "https://api.surfshark.com/"
api_version = "v1"

class AuthorizationRequired(Exception):
    pass


class SurfsharkAPI():
    def __init__(self, tokens=None):
        if tokens is None:
            self.token = None
            self.renew_token = None
        else:
            self.token = tokens["token"]
            self.renew_token = tokens["renewToken"]


    def _get(self, path, *args, version=None, no_auth=False, **kwargs):
        if version is None:
            version = api_version

        if not no_auth:
            if not self.token:
                raise AuthorizationRequired("Call requires authorization")
            kwargs.setdefault("headers", {})
            kwargs["headers"]["Authorization"] = "Bearer " + self.token
        path = api_url + version + "/" + path 
        return requests.get(path, *args, **kwargs)

    def _post(self, path, *args, version=None, no_auth=False, **kwargs):
        if version is None:
            version = api_version

        if not no_auth:
            if not self.token:
                raise AuthorizationRequired("Call requires authorization")
            kwargs.setdefault("headers", {})
            kwargs["headers"]["Authorization"] = "Bearer " + self.token
        path = api_url + version + "/" + path 
        return requests.post(path, *args, **kwargs)


    def getAccountUserMe(self):
        r = self._get("account/users/me")
        j = r.json()
        if "code" in j and j["code"] == 401:
            return None
        return UserResponse(j)


    def getClusters(self):
        # TODO: NoBorders
        # v3 = getNoBordersPortsEnabled
        # if v3:
        #     p1 += "/obfuscated"
        # else:
        #     p1 += "/all"
        #  v3 = getNoBordersCountryCode
        #  v1 = getNoBordersIpsEnabled
        # if v1 and v3:
        #  p1 += "?countryCode=" + v3

        r = self._get("../v4/server/clusters/all")
        return [ServerResponse(x) for x in r.json()]

    def getConnectionInfo(self):
        r = self._get("server/user", no_auth=True, headers={"Cache-Control": "no-cache"})
        return ConnectionInfo(r.json())

    def getCurrentSubscription(self):
        r = self._get("payment/subscriptions/current")
        return r.json()


    def getLinkHash(self):
        r = self._post("account/authorization/link")
        return r.json()

    def getNotifications(self):
        r = self._get("notification/me")
        return r.json()

    def getReferRewards(self):
        r = self._get("referral/referrer/me")
        return r.json()

    def getServerSuggest(self, p1="nearest", p2="", type_=""):
        v0 = "server/suggest"
        # if getNoBordersIpsEnabled:
        #  v0 += "unrestricted"
        #
        if p1 != "nearest":
            v0 += "/foreign"
        else:
            if p2:
                v0 += "/" + p2
        #   if getNoBordersPortsEnabled:
        #       v0 += "?type=obfuscated
        #   elif type_:
            if type_:
                v0 += "?type=" + type_
        
        r = self._get(v0, version="v4")
        return [ServerResponse(x) for x in r.json()]

    def getUserPackages(self):
        r = self._get("server/packages")
        return r.json()

    def getUserSegment(self, visibility, source):
        query = urllib.parse.urlencode({"visibility": visibility, "source": source})
        r = self._get("proposal/feedback?" + query)
        return r.json()

    def renewAuth(self):
        return self.postAuthLogin("renew")

    def postAuthLogin(self, username_or_token, password=None, set_token=True):
        if password is None:
            if username_or_token == "renew":
                username_or_token = self.renew_token
            headers = {"Authorization": "Bearer " + username_or_token}
            r = self._post("auth/renew", no_auth=True, headers=headers)
        else:
            r = self._post("auth/login", no_auth=True, json={"username": username_or_token, "password": password})

        if r.status_code == 401:
            return None

        j = r.json()
        if set_token:
            self.token = j["token"]
            self.renew_token = j["renewToken"]
        return TokenResponse(j)

    def postAutoLoginHash(self, hashcode, set_token=True):
        r = self._post("auth/remote", no_auth=True, json={"hash": hashcode})
        j = r.json()
        if not j:
            return None
        if set_token:
            self.token = j["token"]
            self.renew_token = j["renewToken"]
        return TokenResponse(j)


    def postGeneratePublicKey(self, public_key):
        r = self._post("account/users/public-keys", json={"pubKey": public_key})
        return r.json()

    def postValidatePublicKey(self, public_key):
        r = self._post("account/users/public-keys/validate", json={"pubKey": public_key})
        return r.json()

    def postCreateTvAuthorization(self):
        r = self._post("account/authorization/create", no_auth=True)
        return r.json()

    def postMobileCodeAuthorization(self, code):
        r = self._post("account/authorization/assign", json={"code": code})
        if r.status_code == 200:
            return True
        else:
            return False


    #def deleteServerKey(self, identifier: str):
    #    api = f"server/key/{identifier}"
    #    method = "DELETE"
    #    pass
    #    return KeyInfo

    #def getAbTestList(userId: str, identifier: str, locale: str):
    #    api = "experiments/experiments"
    #    method = "GET"
    #    pass
    #    return AbTest


    #def postAccountUsers(self, ss_lj, registration_request):
    #    r = self._post("account/users", no_auth=True, headers={"ss-lj": ss_lj}, json=registration_request)
    #    return r.json()

    #def postAmazonValidate(self, ss_af, amazon_receipt):
    #    r = self._post("payment/amazon/validate", headers={"ss-af", ss_af} json=amazon_receipt)
    #    return r.json()

    #def postAppRating(self, rating):
    #    r = self._patch(f"proposal/app-rate/{rating}")
    #    return r.json()


    #def postChangePassword(self, password_change_data): #PasswordChangeData
    #    r = self._put("account/users", json=password_change_data)
    #    return r.json() # EmptyResponse


    # shadowsocks
    #def postServerKeyKeepAlive(self, key_request): # KeyRequest
    #    r = self._patch("server/key/keep-alive", json=key_request)
    #    return r.json() # KeyInfo

    #def postCreateGetServerKey(self, key_request): # KeyRequest
    #    r = self._post("server/key", json=key_request)
    #    return r.json() # KeyInfo


    #def getAppRating(self, source):
    #    api = "proposal/app-rate"
    #    method = "GET


    # getLatestVersionInfo
    # getIncidentInfo
    # postMobileCodeAuthorization
    # postPaymentGoogleValidate
    # postPostponeUserRating
    # postTwoFactorAuthorization
    # sendConnectionRating
    # sendFeedbackRejected
    # sendUserFeedback
    # uploadDiagnostics


