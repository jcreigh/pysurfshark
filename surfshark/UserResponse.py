#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .common import JsonObject

class UserResponse(JsonObject):
    class ServiceCredentials(JsonObject):
        def __init__(self, data):
            super().__init__(data)

        def __str__(self):
            return f"ServiceCredentials(username={self.username}, password={self.password})"

    class TwoFactorAuth(JsonObject):
        def __init__(self, data):
            super().__init__(data)

        def __str__(self):
            return f"TwoFactorAuth(active={self.active})"

    class UserServices(JsonObject):
        def __init__(self, data):
            super().__init__(data)

        def __str__(self):
            return f"UserServices(id={self.id}, expiresAt={self.expiresAt}, serviceId={self.serviceId}, isActive={self.isActive})"


    def __init__(self, data):
        super().__init__(data)
        self.data.setdefault("lastLoginAt", None)
        self.data.setdefault("TwoFactorAuth", None)
        self.data.setdefault("daysAfterSignup", None)

        if self.data["twoFactorAuth"] is not None:
            self.data["twoFactorAuth"] = UserResponse.TwoFactorAuth(data["twoFactorAuth"])

        self.data["userServices"] = [UserResponse.UserServices(x) for x in data["userServices"]]
        self.data["serviceCredentials"] = UserResponse.ServiceCredentials(data["serviceCredentials"])

    def __str__(self):
        out = f"UserResponse(id={self.id}, email={self.email}, lastLoginAt={self.lastLoginAt}, serviceCredentials={self.serviceCredentials}, "
        out += f"userServices={self.userServices}, twoFactorAuth={self.twoFactorAuth}, daysAfterSignup={self.daysAfterSignup})"
        return out
