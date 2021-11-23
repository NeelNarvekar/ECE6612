#!/usr/bin/python3

import bluetooth
import requests

def write_addrs(pairs):
    
    web = 'https://bluesmacking.herokuapp.com/write-macs?'
    query = ""
    
    for addr, name in pairs.items():
        query += f"{name}={addr}&"
    
    url = web + query[:-1]
    requests.get(url)

def scan_services():
  print("Scanning for bluetooth devices: ")
  devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)
  number_of_devices = len(devices)
  print(number_of_devices, "devices found")
  pairs = {}
  for addr,name,device_class in devices:
    pairs[addr] = name
    #print("\n")
    #print("Device Name: %s" % (name))
    #print("Device MAC Address: %s" % (addr))
    #print("Device Class: %s" % (device_class))
    #print("Services Found:")
    #services = bluetooth.find_service(address=addr)
    #if len(services) <=0:
    #  print("zero services found on", addr)
    #else:
    #  for serv in services:
    #    print(serv['name'])

  write_addrs(pairs)
  return

#if __name__ == '__main__':
#  scan_services()