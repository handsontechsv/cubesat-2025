import time
import re
import subprocess
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class MyEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory: # Check if it's a file
            print(f"File created: {event.src_path}")
            # Add your notification logic here (e.g., send an email, trigger an alert)
            # Check the file name
            # Json should contain image path, confidence interval, and lat/lon. (More if needed)
            
            # Read the file for power outage alert
            # If alert, send email to operators

            # Perhaps it would be better to move uplink_send to the control loop
            uplink_send()
            pass

def uplink_send():
    print("GS Attempting to send data to satellite")
    satellite_address = "D8:3A:DD:26:D8:B2" #Yujie's Raspberry Pi address is D8:3A:DD:26:D8:B2
    file_path = "ground_station/task_planning.txt"
    RSSI_threshold = -70
    # Subprocess to connect to pi via bluetooth
    # for loop: send a file (placeholder for now) to pi w/ btmgmt and record RSSI
    # if RSSI at a threshold, send a file to the pi via obexftp
    # 
    try:
        #sudo btmgmt find | grep "C4:91:0C:A7:EA:EF" 
        findProcess = subprocess.Popen(["btmgmt", "find"], stdout=subprocess.PIPE, text=True)
        find_process_result = findProcess.stdout.read()
        print("1: " + find_process_result)
        pattern = satellite_address + ".* rssi \-(\d+)"
        rssi_line = re.search(pattern, find_process_result)
        if (rssi_line != None):
            rssi_value = rssi_line.group(1)
            print("REGEX RESULT")
            print(rssi_line)
            print("RSSI VALUE = " + rssi_value)
            
            if (int(rssi_value) > RSSI_threshold):
                #assume you're already paired but not connected

                #may need a loop if multiple files
                send_process = subprocess.Popen(["obexftp", "-b", satellite_address, "-p", \
                                                file_path], \
                                                stdout = subprocess.PIPE, text = True)
                print("Sending a file to ground station!")
                print(send_process.stdout.read())
            
        else:
            print("Device not found!!")
        
        pass
    except KeyboardInterrupt:
        print("Exiting...")



def downlink_recieve():
    path_to_watch = "/Users/yujiewu/Downloads" # Current directory, change to your desired path
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    downlink_recieve()
    