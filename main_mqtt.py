import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
from machine import Pin
import dht
esp.osdebug(None)
import gc
gc.collect()

ssid = 'S.Chaya_2.4G'
password = '1234567890'
mqtt_server = 'broker.hivemq.com'
#EXAMPLE IP ADDRESS or DOMAIN NAME
#mqtt_server = '192.168.1.106'

client_id = ubinascii.hexlify(machine.unique_id())

topic_pub_temp = b'dht/temp'
topic_pub_hum = b'dht/humid'
#topic_pub_led = b'your_name/led/status'

last_message = 0
message_interval = 5

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')

sensor = dht.DHT22(Pin(21))
#sensor = dht.DHT11(Pin(14))
def sub_cb(topic, msg):
    print('from subscribe', msg)
    
def connect_mqtt():
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)
  #client = MQTTClient(client_id, mqtt_server, user=your_username, password=your_password)
  client.set_callback(sub_cb) 
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def read_sensor():
  try:
    sensor.measure()
    temp = sensor.temperature()
    # uncomment for Fahrenheit
    #temp = temp * (9/5) + 32.0
    hum = sensor.humidity()
    if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
      temp = (b'{0:3.1f},'.format(temp))
      hum =  (b'{0:3.1f},'.format(hum))
      return temp, hum
    else:
      return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')

try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    if (time.time() - last_message) > message_interval:
      temp, hum = read_sensor()
      #temp = read_sensor()
      print(temp)
      print(hum)
      client.publish(topic_pub_temp, temp)
      client.publish(topic_pub_hum, hum)
      client.subscribe(topic_pub_led)
      last_message = time.time()
  except OSError as e:
    restart_and_reconnect()
    