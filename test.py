import os
import threading
import time
import sys
import bluetooth

start = time.time()
end = time.time()
pkt_size = 600

def scan_services():
    addrs = ["90:81:58:11:A8:12", "00:1B:41:AA:1E:B0", "D0:81:7A:07:8F:40"]
    for addr in addrs:
        returned_value = os.system(f"sudo l2ping -i hci0 -c 1 -s {pkt_size} {addr}")
        print(returned_value)
    return

if __name__ == '__main__':
    scan_services()



# 88:C6:26:F7:14:4B 
