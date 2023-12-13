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
        
        # Set up external libraries
        self.follower = Follower(self)
        
        # Set up video feed
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID") # video compression
        _date = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        self.video_original = self.create_video_recorder("test_data/tmp/dash%s.avi" % datestr)
        self.video_lane = self.create_video_recorder("test_data/tmp/dash_lane%s.avi" % datestr)
        #self.video_objects = self.create_video_recorder("test_data/tmp/dash_objects%s.avi" % datestr)
        
        logging.info("Setup complete!")
        
    def create_video_recorder(self, path):
        return cv2.VideoWriter(path, self.fourcc, 20.0, (self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))

    def drive(self, speed=__INITIAL_SPEED):
        
        logging.info("Taking off...")
        self.back_wheels.speed = speed
        
        while self.camera.isOpened():
            _, lane_image = self.camera.read()
            #objects = lane_image.copy()
            self.video_original.write(lane_image)
            
            #image_objects = self.process_obstacles(image_objects)
            #self.video_objects.write(image_objects)
            
            lane_image = self.follow(lane_image)
            self.video_lane.write(lane_image)
            show_image("lane lines", lane_image)
            
    def follow(self, image):
        image = self.follower.follow(image)
        return image
                
                
def show_image(title, img, show=True):
    if show:
        cv2.imshow(title, img)


def main():
    with Car() as car:
        car.drive(5)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s:%(asctime)s: %(message)s')
    main()