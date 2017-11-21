import time
from beacontools import parse_packet
from beacontools import BeaconScanner, IBeaconFilter
import math

UUID_BLUE =   "b9407f30-f5f8-466e-aff9-00012345678b"
UUID_PURPLE = "b9407f30-f5f8-466e-aff9-25556b57fe6e"
UUID_GREEN =  "b9407f30-f5f8-466e-aff9-0000025556b5"

scanners = [BeaconScanner]*1

# scan for all iBeacon advertisements from beacons with the specified uuid
def init(UUIDS, callback):
  scanners = [BeaconScanner]*len(UUIDS)
  i = 0
  for scanner in scanners:
    scanner = BeaconScanner(callback,
      device_filter=IBeaconFilter(uuid=UUIDS[i])
    )
    scanner.start()
    i = i + 1

def destroy():
  for scanner in scanners:
    scanner.stop()
    

#exemplo função de callback
#def callback1(bt_addr, rssi, packet, additional_info):
#    if packet.uuid == UUID_BLUE:
#      print("Você está próximo do beacon blue")
#    elif packet.uuid == UUID_PURPLE:
#      print("Você está próximo do beacon purple")
#    elif packet.uuid == UUID_GREEN:
#      print("Você está próximo do beacon green")

#exemplo de como utilizar
#init([UUID_BLUE,UUID_GREEN,UUID_PURPLE],callback1)
#time.sleep(100)
#destroy()