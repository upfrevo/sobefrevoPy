import time
from beacontools import BeaconScanner, EddystoneEncryptedTLMFrame, EddystoneFilter

def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

# scan for all TLM frames of beacons in the namespace "12345678901234678901"
scanner = BeaconScanner(callback,
    device_filter=EddystoneFilter(namespace="edd1ebeac04e5defa017"),
    packet_filter=EddystoneEncryptedTLMFrame
)
scanner.start()

time.sleep(10)
scanner.stop()
