try:
    import usocket as socket
except:
    import socket

from machine import Pin
import network
import dht
import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'S.Chaya_2.4G'
password = '1234567890'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

sensor = dht.DHT22(Pin(21))