import os
import threading
import time
import sys
import bluetooth

start = time.time()
end = time.time()

def scan_services():
    start = time.time()
    packages_size = 600
    deviceSet = set()
    serviceDict = {}
    smackableDevices = 0
    try:
        while True:
            print("Scanning for bluetooth devices: ")
            devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)
            number_of_devices = len(devices)
            print(number_of_devices, "devices found")
            for addr,name,device_class in devices:                
                returned_value = os.system('sudo l2ping -i hci0 -c 1 -s ' + str(packages_size) + " " + addr)
                print('returned value:', returned_value)
                if returned_value != 256 and addr not in deviceSet:
                    deviceSet.add(addr)
                    smackableDevices = smackableDevices + 1

                    print("\n")
                    print("Device Name: %s" % (name))
                    print("Device MAC Address: %s" % (addr))
                    print("Device Class: %s" % (device_class))
                    print("Services Found:")

                    services = bluetooth.find_service(address=addr)
                    if len(services) <=0:
                        print("zero services found on", addr)
                    else:
                        for serv in services:
                            if serv['name'] in serviceDict:
                                serviceDict[serv['name']] += 1
                            else:
                                serviceDict[serv['name']] = 1
                            print(serv['name'])
                        print("\n")
            time.sleep(0.1)
    except KeyboardInterrupt:
        end = time.time()
        f = open("analysisResults.txt", "w")
        f.write(str(len(deviceSet)) + " unique devices found in " + str((end - start)/60) + " minutes\n")
        f.write(str(smackableDevices) + "/" + str(len(deviceSet)) + " devices respond to requests\n")
        for key,val in serviceDict.items():
            if key != None and val != None:
                f.write(f"{key} : {val}\n")
        f.close()
    return

if __name__ == '__main__':
    scan_services()



# 88:C6:26:F7:14:4B 