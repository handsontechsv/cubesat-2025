import bluetooth
import select
import time

class GroundStationDiscoverer(bluetooth.DeviceDiscoverer):

    def __init__(self, ground_station_address, device_id=-1):
        self.ground_station_address = ground_station_address
        self.ground_station_rssi = None
        bluetooth.DeviceDiscoverer.__init__(self, device_id)

    def pre_inquiry(self):
        self.done = False

    def device_discovered(self, address, device_class, rssi, name):
        print(f"Find device at address {address} of class {device_class} with rssi {rssi}: {name}")
        if(address == self.ground_station_address):
            self.ground_station_rssi = rssi

    def inquiry_complete(self):
        self.done = True


def find_device_rssi(address):
    d = GroundStationDiscoverer(ground_station_address = address)
    d.find_devices(duration=10, lookup_names=True)

    readfiles = [ d, ]
    begin_time = time.time()
    while True:
        current_time = time.time()
        rfds = select.select(readfiles, [], [])[0]
        if d in rfds:
            d.process_event()
        if d.done:
            break
        if d.ground_station_rssi or current_time - begin_time > 10:
            if(current_time - begin_time > 10):
                print("Device not found, timeout")
            d.cancel_inquiry()
            break
    return d.ground_station_rssi
      