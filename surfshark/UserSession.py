#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .API import SurfsharkAPI, AuthorizationRequired

class UserSession():
    def __init__(self, tokens=None):
        self.api = SurfsharkAPI(tokens=tokens)
        self.tokens = None
        self.logged_in = False

    def login(self, username, password):
        self.tokens = self.api.postAuthLogin(username, password)
        if self.tokens:
            return True
        return False

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


