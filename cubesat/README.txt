CUBESAT BLUETOOTH SETUP

the current OS i'm using is bookworm pls upgrade to it

in terminal, do sudo nano /etc/rc.local and copy the contents of the rc.local in this git
THEN make rc.local executable by chmod a+x /etc/rc.local
If you do ls -l /etc/rc.local it should say something like -rwxr-xr-x which means all users can execute it
sudo reboot to see if it runs
check the log file in /home/raspberrypi/cubesat-2025/cubesat/log.txt to see if it is printing stuff by doing tail -F /home/raspberrypi/cubesat-2025/cubesat/log.txt

Also install bluez using apt install python3-PyBluez




Reguarding the cubesat control loop:

Downlinking
* each power outage produces 1 processed image and 1 metadata file (json or other) that contains image name, lat, lon, time, confidence interval
* treat each file as individual sends and delete each file from files_to_send when it successfully sends
* ground station will combine the recieved metadata file into one big json and save the outage images

MAIN
Read task plan:
* check if task plan file exists
* if task exists, replace all old tasks, and delete it
* a list of times to take pictures for the future (can be one orbit or multiple orbits)
    * time is recorded by OS TIME OF THE CUBESAT WHEN IT SHOULD TAKE THE PHOTO (current time.time() + x seconds)
* prepare for image Capture
    Check if time matches task plan
    * use current time, search for task times on the task list within range
    * delete the matched time (or mark as invalid some other way) when completed


Parallel thread 1: Image Capture (a new subprocess starts every time the time matches)
    * Image capture should store the image in a directory that is not files_to_send, somewhere for image process to access
        * ie a database or another folder (i believe saving it to a folder takes a long time to download)
    Next run outage detection pipeline:  Image processing --> outage detection --> store into database 
    * if an image has been captured / show up in directory (call subprocess command line to see if a file w/ such a name exists?)
        * When new image is added, run image processing pipeline
        * copy image (if outage) and metadata to files_to_send folder

Parallel Thread 2:
    Read RSSI either IF there are files to send OR if task plan has not been updated for 2-3 minutes
        alternatively: frequently read RSSI when afar, but when close to gs decrease RSSI reading frequency
    if its close to gs:as
        send the file down
        recieve task plan file

to do parallel stuff: subprocess
control loop initializes subprocess to monitor rssi and sending values
main loop detects if file has been recieved and do the rest of the program
- run n image processing subprocesses for n images


Optional: Lock mechanism:
    If downlinking, prevent modifications to data in files_to_send
    If finishing image_processing and in the process of copying files to files_to_send, that file cannot be downlinked