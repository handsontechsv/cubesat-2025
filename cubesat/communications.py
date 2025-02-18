import re
import time
import os
import subprocess
import BlueToothDiscover

def main():
    ground_station_address = "C4:91:0C:A7:EA:EF" #Yujie's mac address is C4:91:0C:A7:EA:EF
    files_to_send_dir = "/home/raspberrypi/cubesat-2025/cubesat/files_to_send"
    recieve_path = "/home/raspberrypi/cubesat-2025/cubesat/recieved_files"
    gs_tasks_path = "cubesat_task_plan.txt"
    RSSI_threshold = -70
    # Subprocess to connect to pi via bluetooth
    # for loop: send a file (placeholder for now) to pi w/ btmgmt and record RSSI
    # if RSSI at a threshold, send a file to the pi via obexftp
    # 
    try:
        while True:
            #check if task info file has not been updated for 2 mins OR if there are files in files_to_send
            if (time.time() - os.path.getmtime(recieve_path) < 10 and len(os.listdir("/home/raspberrypi/cubesat-2025/cubesat/files_to_send")) <= 0):
                time.sleep(10)
                continue
            print("Reading RSSI to see if the CubeSat is over Ground Station:")
            #not verified to work!!
#            findProcess = subprocess.Popen(["/usr/bin/btmgmt", "find"], stdout=subprocess.PIPE, stderr = subprocess.PIPE, text=True, cwd = "/home/raspberrypi")
#            fp_std_out, fp_std_err = findProcess.communicate()

            rssi_value = BlueToothDiscover.find_device_rssi(ground_station_address)
            print(f"rssi_value is {rssi_value}")
            if (rssi_value != None):
                if (rssi_value > RSSI_threshold):
                    #assume you're already paired but not connected
                    print("Ground station found!")

                    #loop through every file in the files_to_send folder
                    for file in os.listdir(files_to_send_dir):
                        print("Sending an orbit result file to ground station!")
                        print(file)
                        send_process = subprocess.Popen(["/usr/bin/obexftp", "-b", ground_station_address, "-p", \
                                                        files_to_send_dir + "/" + file], \
                                                        stdout = subprocess.PIPE, stderr = subprocess.PIPE,\
                                                        text = True)
                        stdout, stderr = send_process.communicate()
                        #print(stdout)
                        #verify if file was sent successfully
                        #returncode doesn't work, so regex the output...
                        if (send_process.returncode == 0 or send_process.returncode == 255):
                            print("Orbit result file " + file+ " sent successfully!")
                            #delete the file just sent, or mark it invalid
                            os.remove(files_to_send_dir + "/" + file)
                            print("sent file deleted")
                        else:
                            print("Orbit result file " + file+ " NOT sent successfully! (will attempt next orbit)")

                    print("Now fetching assignment file from the ground station")
                    #This can only fetch from the Downloads Folder or whichever folder is public for bluetooth sharing!!!
                    fetch_process = subprocess.Popen(["obexftp", "-b", ground_station_address, \
                                                    "-g", gs_tasks_path], \
                                                    stdout = subprocess.PIPE, cwd = recieve_path, text = True)
                    print(fetch_process.stdout.read())
                    print("Assignment file recieved.")
                            
                    print("CUBESAT LEAVES GROUND STATION.")
                    print("Ground station disconnect Bluetooth")
                else:
                    print("RSSI connection too weak - CubeSat not close to Ground station, no bluetooth connection established")
                
            else:
                print("CubeSat not close to Ground station, no bluetooth connection established")
                
            time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting...")

        

if __name__== "__main__": 
    main()
