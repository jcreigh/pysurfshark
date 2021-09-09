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


def getMainPublicKey():
    import subprocess
    try:
        main_pubkey = subprocess.check_output(["dig", "+short", "TXT", "wgs.prod.surfshark.com"]).strip()[13:-2].decode()
    except FileNotFoundError:
        try:
            output = subprocess.check_output(["nslookup", "-q=txt", "wgs.prod.surfshark.com"])
            main_pubkey = output.split(b'public_key', 1)[1].split(b']', 1)[0][1:]
        except FileNotFoundError:
            raise RuntimeError('Could not lookup Surfshark\'s main public key. Install dig or nslookup')

    return main_pubkey
