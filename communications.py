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
            findProcess = subprocess.Popen(["btmgmt", "find"], stdout=subprocess.PIPE, text=True)
            grepProcess = subprocess.Popen(["grep", ground_station_address], stdin = findProcess.stdout, stdout = subprocess.PIPE, text = True)
            print("1: " + findProcess.stdout.read() + " 2: " + grepProcess.stdout.read())
            print(type( grepProcess.stdout.read()))
            
            pass
    except KeyboardInterrupt:
        print("Exiting...")


if __name__== "__main__": 
    main()