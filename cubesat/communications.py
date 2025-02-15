import re
import subprocess

def downlink_send():
    print("Hello, World!")
    ground_station_address = "C4:91:0C:A7:EA:EF" #Yujie's mac address is C4:91:0C:A7:EA:EF
    file_path = "/home/raspberrypi/cubesat-2025/cubesat/files_to_send/placeholder.txt"
    recieve_path = "/home/raspberrypi/cubesat-2025/cubesat/recieved_files"
    gs_tasks_path = "haha.txt"
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

                print("Now fetching file from the ground station")
                #This can only fetch from the Downloads Folder or whichever folder is public for bluetooth sharing!!!
                fetch_process = subprocess.Popen(["obexftp", "-b", ground_station_address, \
                                                "-g", gs_tasks_path], \
                                                stdout = subprocess.PIPE, cwd = recieve_path, text = True)
            
        else:
            print("Device not found!!")
        
        pass
    except KeyboardInterrupt:
        print("Exiting...")

        

if __name__== "__main__": 
    downlink_send()
