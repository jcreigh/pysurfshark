#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .common import JsonObject

class TokenResponse(JsonObject):
    def __init__(self, data):
        super().__init__(data)

    def __str__(self):
        return f"TokenResponse(token={self.token}, renewToken={self.renewToken})"
