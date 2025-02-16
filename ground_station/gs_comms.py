import time
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
            # Json should contain image path, confidence interval, and lat/lon. (More if needed)
            
            # Read the file for power outage alert
            # If alert, send email to operators
            pass

def downlink_recieve():
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


if __name__ == "__main__":
    downlink_recieve()
    