import time
import communications
import adcs
#import take_picture
import subprocess
import os

def get_task_times(old_task_times):
    if os.path.exists("/home/raspberrypi/cubesat-2025/cubesat/recieved_files/cubesat_task_plan.txt"):
        task_times_new = []
        with open("/home/raspberrypi/cubesat-2025/cubesat/recieved_files/cubesat_task_plan.txt", "r") as file:
            #TODO: if the file format is invalid, ignore the file instead of producing error
            for line in file:
                #TODO: remove the + time.time() and make the task plan file return a time since epoch instead
                task_times_new.append(int(line) + time.time())
        #delete the file after finished
        os.remove("/home/raspberrypi/cubesat-2025/cubesat/recieved_files/cubesat_task_plan.txt")
        print("Task info loaded")
        return task_times_new
    else:
        return old_task_times

def temp_file_adder():
    file_dir = "/home/raspberrypi/cubesat-2025/cubesat/files_to_send"
    file_name = "placeholder" + str(time.time()) +".txt"
    path = file_dir+"/"+file_name
    with open(path, "w") as file:
        file.write("placeholder for the images")
    print("New image created")
    #ls_process = subprocess.Popen(["ls"], cwd = file_dir, text = True)
    #print(ls_process.stdout.read())

def main():
    print("CubeSat OPERATION BEGIN")
    #init RSSI / ground station detection subprocess
    comms_sp = subprocess.Popen(["python3", "-u", "/home/raspberrypi/cubesat-2025/cubesat/communications.py"], text = True)
    last_cycle_time = time.time()
    task_times = [] #may be updated via task plan from ground station
    fake = 0
    try:
        while True:
            #Update the task_times list if the task plan file exists
            #task_times = get_task_times() #see above for format
            task_times = get_task_times(task_times)
            time.sleep(1)
            #print(f"Next task times: {task_times}")
            #(fake)
            # Track the CubeSat's location
            #print("CubeSat is tracking location")
            
            # If CubeSat time is within 10 seconds of an item in task_times, take a picture
            for task_time in task_times:
                current_time = time.time()
                if(abs(task_time - current_time) < 10):
                    print(f"CubeSat reached location at time {current_time}, begin taking picture")
                    #take_picture.take_photo()
                    # create a subprocess to take picture and process it
                    # subprocess.Popen(["python3", "take_picture.py"]) <-- this, but take_picture needs to include the processing
                    if fake == 1:
                        print("\n  !! OUTAGE DETECTED !!  \n")
                        temp_file_adder()
                    else :
                        fake = 1
                        print("\n      No outage \n")
                    #delete the task_time from task_times
                    task_times.remove(task_time)
                
            #Results of RSSI subprocessprint(comms_sp.stdout.readline())
            last_cycle_time = time.time()
            #print("Loop end at " + str(last_cycle_time))
            
    except KeyboardInterrupt:
        print("CubeSat Stopped")

if __name__== "__main__":
    main()
