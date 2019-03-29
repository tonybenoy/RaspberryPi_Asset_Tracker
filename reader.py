#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2018, Tony Benoy <me@tonybenoy.com>

import redis
from time import sleep
import pymysql
import json
r = redis.Redis()
database = "myDataBase"
host = "localhost"
username = "username"
passwd = "password"
device_id = "b8:27:eb:eb:ab:57"
olddata = []
while True:
    conn = pymysql.connect( host,username,passwd,database) 
    cur = conn.cursor()
    print("______")
    newdata = r.lrange("data",0,r.llen("data"))
    for a in newdata:
        print (a)
        item = json.loads(a.decode("utf-8"))
        print (item)
        cur.execute("INSERT INTO BLE(time,date,uuid,minor,major,address,power,rssi,device_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (str(item["time"]),str(item["date"]),str(item["uuid"]),item["minor"],item["major"],str(item["address"]),item["power"],item["rssi"],device_id))
    data = [item for item in newdata if item not in olddata]
    olddata = newdata    
    print (data)
    conn.commit()
    conn.close()
