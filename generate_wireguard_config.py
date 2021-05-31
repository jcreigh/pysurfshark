#!/usr/bin/env python
# -*- coding: utf-8 -*-

from surfshark.UserSession import UserSession
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

    if not sess.login(username, password):
        print("Login failed")
        exit(1)

print("Logged in")
wg_pubkey = input("Wireguard pubkey: ")
sess.api.postGeneratePublicKey(wg_pubkey)

servers = sess.api.getClusters()
servers = [x for x in servers if x.pubKey is not None]
for i, s in enumerate(servers):
    print(f"{i} {s.country} {s.location}")

num = int(input("Enter location number: "))
server = servers[num]

import subprocess
main_pubkey = subprocess.check_output(["dig", "+short", "TXT", "wgs.prod.surfshark.com"]).strip()[13:-2].decode()

print(f"""
[Interface]
Address = 10.14.0.2/16
PrivateKey =

[Peer]
PublicKey = {main_pubkey}
AllowedIPs = 172.16.0.36/32
EndPoint = wgs.prod.surfshark.com:51820

[Peer]
PublicKey = {server.pubKey}
AllowedIPs =
EndPoint = {server.connectionName}:51820
""")

[]
