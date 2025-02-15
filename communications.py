import re
import subprocess

def main():
    print("Hello, World!")
    ground_station_address = "C4:91:0C:A7:EA:EF" #Yujie's mac address
    file_path = ""
    current_RSSI = 0
    RSSI_threshold = -70
    # TODO: subprocess to connect to pi via bluetooth
    # for loop: send a file (placeholder for now) to pi w/ btmgmt and record RSSI
    # if RSSI at a threshold, send a file to the pi via obexftp
    # 
    try:
        #sudo btmgmt find | grep "C4:91:0C:A7:EA:EF" 
        findProcess = subprocess.Popen(["btmgmt", "find"], stdout=subprocess.PIPE, text=True)
        grepProcess = subprocess.Popen(["grep", ground_station_address], stdin = findProcess.stdout, stdout = subprocess.PIPE, text = True)
        find_process_result = findProcess.stdout.read()
        print("1: " + find_process_result)
        pattern = ground_station_address + ".* rssi \-(\d+)"
        rssi_line = re.search(pattern, find_process_result)
        if (rssi_line != None):
            rssi_value = rssi_line.group(1)
            print("REGEX RESULT")
            print(rssi_line)
            print("RSSI VALUE = " + rssi_value)
            
            #assume you're already paired but not connected
            send_process = subprocess.Popen(["obexftp", "-b", ground_station_address, "-p", \
                                             "/home/raspberrypi/cubesat-2025/communications.py"], \
                                            stdout = subprocess.PIPE, text = True)
            print("Sending a file to ground station!")
            print(send_process.stdout.read())
            
        else:
            print("Device not found!!")
        
        pass
    except KeyboardInterrupt:
        print("Exiting...")


if __name__== "__main__": 
    main()
