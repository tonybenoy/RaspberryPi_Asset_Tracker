#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2018, Tony Benoy <me@tonybenoy.com>

from __future__ import print_function
import time
import sys
import json
import datetime
from bluetooth.ble import BeaconService, GATTRequester, GATTResponse
import redis
def jsongen(data,add):
    return json.dumps({"time" : str(datetime.datetime.utcnow().time()),
     "date" : str(datetime.datetime.utcnow().date()),
     "uuid" : data[0],
     "minor" : data[2],
     "major" : data[1],
     "address" : add,
     "power" : data[3],
     "rssi" : data[4]
     })
r = redis.Redis()
r.delete("data")
service =BeaconService()
while True:
    devices = service.scan(1)
    for address, data in list(devices.items()):
        r.lpush("data",str(jsongen(data,address)))
        r.ltrim("data",0,5000)
        print(jsongen(data,address))
