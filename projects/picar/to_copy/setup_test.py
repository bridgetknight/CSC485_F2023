import picar
import cv2
import datetime
import logging
from right_lane_follower import Follower
#from stimuli import StimuliProcessor

class Car(object):
    
    __INITIAL_SPEED = 0
    __SCREEN_WIDTH = 320
    __SCREEN_HEIGHT = 240
    
    def __init__(self):
        # Set up camera, wheels
        logging.info("Setting up Picar...")
        
        picar.setup()
        
        logging.debug("Setting up camera")
        #self.camera = picamera.PiCamera()
        self.camera = cv2.VideoCapture(-1) # REVISE
        self.camera.set(3, self.__SCREEN_WIDTH)
        self.camera.set(4, self.__SCREEN_HEIGHT)
    
        logging.debug("Setting up rear wheels")
        self.back_wheels = picar.back_wheels.Back_Wheels()
        self.back_wheels.speed = 0 # range 0-40
        
        logging.debug("Setting up front wheels")
        self.front_wheels = picar.front_wheels.Front_Wheels()
        #self.front_wheels.turning_offset = 60
        self.front_wheels.turn(90)