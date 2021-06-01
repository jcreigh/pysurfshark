#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .API import SurfsharkAPI, AuthorizationRequired

class UserSession():
    FAIL = 0
    SUCCESS = 1
    NEED_2FA = 2

    def __init__(self, tokens=None):
        self.api = SurfsharkAPI(tokens=tokens)
        self.tokens = None
        self.logged_in = False

    def login(self, username, password):
        self.tokens = self.api.postAuthLogin(username, password)
        if self.tokens is not None:
            if self.tokens[1]:
                return UserSession.SUCCESS
            return UserSession.NEED_2FA
        return UserSession.FAIL

    def submit2FA(self, code):
        return self.api.postTwoFactorAuthorization(code)

    def renewToken(self):
        self.tokens = self.api.renewAuth()
        if self.tokens:
            return True
        return False

    def isLoggedIn(self):
        try:
            return self.api.getAccountUserMe() is not None
        except AuthorizationRequired:
            return False


