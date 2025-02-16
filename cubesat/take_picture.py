from picamera2 import Picamera2
import image_processing as model
import time

picam2 = Picamera2()

i = 0
def img_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    global i
    i += 1
    t = time.strftime("_%H%M%S")
    imgname = name + str(i) + t + ".jpg"
    return imgname


def take_photo():
    """
    This function is NOT complete. Takes a photo when the FlatSat is shaken.
    Replace psuedocode with your own code.
    """
    #while True:
        #accelx, accely, accelz = accel_gyro.acceleration

        #CHECKS IF READINGS ARE ABOVE THRESHOLD
            #PAUSE
            #name = ""     #First Name, Last Initial  ex. MasonM
            #TAKE PHOTO
            #PUSH PHOTO TO GITHUB
        
        #PAUSE
        #if accelx > THRESHOLD:
    name = img_gen("test")
    picam2.start_and_capture_file(name, delay=1, show_preview=False)
    return name

def main():
    take_photo()


if __name__ == '__main__':
    try:
        while True:
            path = take_photo()
            print("after taking photo: "+ time.strftime("_%H%M%S"))
            print(model.main(path))
            print("after processing: "+ time.strftime("_%H%M%S"))
    except KeyboardInterrupt:
        print("Fin.")

