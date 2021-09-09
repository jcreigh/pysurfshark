#!/usr/bin/env python
# -*- coding: utf-8 -*-

from surfshark.UserSession import UserSession
from surfshark import getMainPublicKey
from getpass import getpass
import time

sess = UserSession()

username = input("Username (blank for tv code login): ")
if not username:
    r = sess.api.postCreateTvAuthorization()
    print(f"Code: {r['code']}")
    print("Waiting... ", end="", flush=True)
    while not sess.api.postAutoLoginHash(r['hash']):
        time.sleep(2)
else:
    password = getpass()

    ret = sess.login(username, password)
    if ret == UserSession.FAIL:
        print("Failed")
        exit(1)
    elif ret == UserSession.NEED_2FA:
        print("2FA Required")
        while 1:
            code = input("Code: ")
            if sess.submit2FA(code):
                break
            print("Failed, try again")

print("Logged in")
wg_pubkey = input("Wireguard pubkey: ")
sess.api.postGeneratePublicKey(wg_pubkey)

servers = sess.api.getClusters()
servers = [x for x in servers if x.pubKey is not None]
for i, s in enumerate(servers):
    print(f"{i} {s.country} {s.location}")

num = int(input("Enter location number: "))
server = servers[num]

main_pubkey = getMainPublicKey()

print(f"""
[Interface]
Address = 10.14.0.2/16
PrivateKey =

[Peer]  # Surfshark: Main Server
PublicKey = {main_pubkey}
AllowedIPs = 172.16.0.36/32
EndPoint = wgs.prod.surfshark.com:51820

[Peer]  # Surfshark: {server.country} {server.location}
PublicKey = {server.pubKey}
AllowedIPs =
EndPoint = {server.connectionName}:51820
""")

