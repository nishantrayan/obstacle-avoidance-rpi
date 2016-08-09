# sudo python testblescan.py 2.38  | grep "e6:46:2d:29:12:e2"
# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys

import bluetooth._bluetooth as bluez
MAC_LIST = ['e6:46:2d:29:12:e2']
DATA_POINTS = 50
class KalmanFilter(object):

    def __init__(self, process_variance, estimated_measurement_variance):
        self.process_variance = process_variance
        self.estimated_measurement_variance = estimated_measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def input_latest_noisy_measurement(self, measurement):
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance

        blending_factor = priori_error_estimate / (priori_error_estimate + self.estimated_measurement_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

    def get_latest_estimated_measurement(self):
        return self.posteri_estimate


def distance(rssi):
  if (rssi == 0):
    return -1.0
  tx_power = -59
  return pow(10, (1.0 * (tx_power - rssi) / 20))

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

rssi_values = []
while True:
	returnedList = blescan.parse_events(sock, 10)
	for beacon in returnedList:
          b = beacon.split("|")[0]
          if(b in MAC_LIST):
            rssi_values.append(int(beacon.split("|")[1]))
            if(len(rssi_values) >= DATA_POINTS):
              print "Acquired", DATA_POINTS, "values"
              filter = KalmanFilter(1,3)
              for rssi in rssi_values:
                print rssi      
                filter.input_latest_noisy_measurement(rssi)
              estimated_rssi = filter.get_latest_estimated_measurement()  
              print estimated_rssi 
              print distance(estimated_rssi)  
              rssi_values = []
                        
