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
        while True:
            #sudo btmgmt find | grep "C4:91:0C:A7:EA:EF" 
            something = subprocess.Popen(["sudo", "btmgmt",  "|", "grep", ground_station_address], stdout=subprocess.PIPE, text=True)
            print(something.stdout.read())
            pass
    except KeyboardInterrupt:
        print("Exiting...")


if __name__== "__main__": 
    main()