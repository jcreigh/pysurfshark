#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .common import JsonObject

class ServerResponse(JsonObject):
    class Coordinates(JsonObject):
        def __init__(self, data):
            super().__init__(data)
            self.data.setdefault("longitude", None)
            self.data.setdefault("latitude", None)

    class Entry(JsonObject):
        def __init__(self, data):
            super().__init__(data)
            self.data.setdefault("value", None)

    class Info(JsonObject):
        def __init__(self, data):
            super().__init__(data)
            self.data.setdefault("id", None)
            self.data.setdefault("entry", None)

            if self.data["entry"] is not None:
                self.data["entry"] = ServerResponse.Entry(self.data["entry"])

    def __init__(self, data):
        super().__init__(data)
        self.data.setdefault("pubKey", "")
        self.data.setdefault("info", [])
        self.data.setdefault("coordinates", None)
        self.data.setdefault("transitCluster", None)

        if "info" in data and isinstance(data["info"], dict):
            self.data["info"] = [self.data["info"]]
        self.data["info"] =  [ServerResponse.Info(x) for x in self.data["info"]]

        if self.data["coordinates"] is not None:
            self.data["coordinates"] = ServerResponse.Coordinates(self.data["coordinates"])

        if self.data["transitCluster"] is not None:
            self.data["transitCluster"] = ServerResponse(self.data["transitCluster"])
