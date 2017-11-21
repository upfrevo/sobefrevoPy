import time 
from beacontools import parse_packet 
from beacontools import BeaconScanner, IBeaconFilter
import math

def callback(bt_addr, rssi, packet, additional_info):
    #adv = parse_packet(packet)
    print(packet.tx_power)
    print(rssi)
    ratio = rssi * 1 /packet.tx_power
    #print(ratio)
    dist = -1
    if ratio < 1.0:
      dist = math.pow(ratio, 10)
    else:
      dist = (0.89976) * math.pow(ratio, 7.7095) + 0.111
    
    print(dist)
    #if (ratio < 1.0) {
    #   return Math.pow(ratio, 10);
    #} else {
    #   return (0.89976) * Math.pow(ratio, 7.7095) + 0.111;
    #}
    #print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

UUID_BLUE = "b9407f30-f5f8-466e-aff9-25556b57fe6d"
UUID_PURPLE = "b9407f30-f5f8-466e-aff9-25556b57fe6e"
# scan for all iBeacon advertisements from beacons with the specified uuid
scanner = BeaconScanner(callback,
    device_filter=IBeaconFilter(uuid=UUID_PURPLE)
)
scanner.start()
time.sleep(5)
scanner.stop()
