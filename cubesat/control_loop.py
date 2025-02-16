import time
import communications
import adcs
import take_picture
import subprocess
import os

def get_task_times():
    #TODO: modify this to match the correct file format we are using!!
    '''
    if os.path.exists("cubesat/recieved_files/task_plan.txt"):
        task_times = []
        with open("task_plan.txt", "r") as file:
            for line in file:
                task_times.append(int(line))
        #delete the file after finished
        os.remove("task_plan.txt")
        return task_times
    '''

def main():
    #init RSSI / ground station detection subprocess
    subprocess.Popen(["python3", "communications.py"])
    last_cycle_time = time.time()
    task_times = [] #may be updated via task plan from ground station
    try:
        while True:
            #Update the task_times list if the task plan file exists
            #task_times = get_task_times() #see above for format
            time.sleep(0.5)
            # Track the CubeSat's location
            print("CubeSat is tracking location")
            # If CubeSat time is within 10 seconds of an item in task_times, take a picture
            for task_time in task_times:
                if(task_time - last_cycle_time < 10):
                    print("CubeSat reached location, begin taking picture")
                    #take_picture.take_photo()
                    # create a subprocess to take picture and process it
                    # subprocess.Popen(["python3", "take_picture.py"]) <-- this, but take_picture needs to include the processing
                #delete the task_time from task_times
                task_times.remove(task_time)
            last_cycle_time = time.time()
            
    except KeyboardInterrupt:
        print("CubeSat Stopped")

if __name__== "__main__":
    main()