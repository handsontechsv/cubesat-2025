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
            if(event.src_path == "task_planning.txt"):
                # File should list the next times to take pictures
                # Save the information somewhere to be used by the satellite
                
                pass

def downlink_send():
    print("Hello, World!")
    ground_station_address = "C4:91:0C:A7:EA:EF" #Yujie's mac address is C4:91:0C:A7:EA:EF
    file_path = "/home/raspberrypi/cubesat-2025/local_database/placeholder.txt"
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
        pattern = ground_station_address + ".* rssi \-(\d+)"
        rssi_line = re.search(pattern, find_process_result)
        if (rssi_line != None):
            rssi_value = rssi_line.group(1)
            print("REGEX RESULT")
            print(rssi_line)
            print("RSSI VALUE = " + rssi_value)
            
            if (int(rssi_value) > RSSI_threshold):
                #assume you're already paired but not connected

                #may need a loop if multiple files
                send_process = subprocess.Popen(["obexftp", "-b", ground_station_address, "-p", \
                                                file_path], \
                                                stdout = subprocess.PIPE, text = True)
                print("Sending a file to ground station!")
                print(send_process.stdout.read())
            
        else:
            print("Device not found!!")
        
        pass
    except KeyboardInterrupt:
        print("Exiting...")

        

def uplink_recieve():
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
   

if __name__== "__main__": 
    downlink_send()
