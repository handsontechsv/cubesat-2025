import time
import communications
import adcs
import take_picture

def main():
    #init RSSI / ground station detection subprocess
    last_cycle_time = time.time()
    task_times = [] #may be updated via task plan from ground station
    try:
        while True:
            last_photo_time = time.time()
            time.sleep(0.5)
            # Track the CubeSat's location
            print("CubeSat is tracking location")
            # If CubeSat time is within 10 seconds of an item in task_times, take a picture
            for task_time in task_times:
                if(task_time - last_cycle_time < 10):
                    print("CubeSat reached location, begin taking picture")
                    #take_picture.take_photo()
                    # create a subprocess to take picture and process it
                    continue
            last_cycle_time = time.time()
            
    except KeyboardInterrupt:
        print("CubeSat Stopped")

if __name__== "__main__":
    main()