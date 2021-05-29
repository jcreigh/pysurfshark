#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from collections import UserDict

class JsonObject(UserDict):
    def __init__(self, data):
        super().__init__(data)

    def __getattr__(self, attr):
        if attr in self.data:
            return self.data[attr]
        return self.__getattribute__(attr)

    #def __setattr__(self, attr, value):
    #    if attr != "data" and attr in self.data:
    #        self.data[attr] = value
    #    else:
    #        object.__setattr__(self, attr, value)
