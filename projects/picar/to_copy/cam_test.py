from picamera import PiCamera 
from time import sleep
import numpy as np 
import cv2

if __name__ == "__main__":

    with picamera.PiCamera() as cam:
        # camera settings
        cam.resolution = (320, 240)
        cam.framerate = 24

        # wait
        time.sleep(2)

        # take image
        img = np.empty((240 * 320 * 3,), dtype = np.uint8)
        cam.capture(out, "bgr")
        img = img.reshape((240, 320, 3))

        plt.axis("off")
        plt.imshow(img)