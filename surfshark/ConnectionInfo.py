#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .common import JsonObject

def ConnectionInfo(JsonObject):
    def __init__(self, data):
        super().__init__(data)

    def __str__(self):
        out = f"ConnectionInfo(ip={self.ip}, isp={self.isp}, countryCode={self.countryCode}, country={self.country}, "
        out += f"city={self.city}, secured={self.secured}, restricted={self.restricted})"
        return out

