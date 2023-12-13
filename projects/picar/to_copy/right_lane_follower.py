import cv2
import numpy as np
import math
import datetime
import sys
import matplotlib.image

_SHOW_IMAGE = False

class Follower(object):

    def __init__(self, car = None):
        self.car = car
        self.curr_steering_angle = 90

    def follow(self, img):
        show_img("orig", img)
       # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        lane_lines, img = detect_lane(img)

        final_img = self.steer(img, lane_lines)

        return final_img

    def steer(self, img, lane_lines):
        if len(lane_lines) == 0:
            return img
        new_steering_angle = compute_steering_angle(img, lane_lines)
        print(f"new angle: {new_steering_angle}")
        print(f"old angle: {self.curr_steering_angle}")
        self.curr_steering_angle = stabilize_steering_angle(self.curr_steering_angle, new_steering_angle, len(lane_lines))        
        #self.curr_steering_angle = new_steering_angle
        print(f"new2 angle: {self.curr_steering_angle}")
        
        if self.car is not None:
            self.car.front_wheels.turn(self.curr_steering_angle)
        
        curr_img = display_heading_line(img, self.curr_steering_angle)
        show_img("heading", curr_img)

        return curr_img
        
def detect_lane(img):
    edges = detect_edges(img)
    show_img("edges", edges)

    cropped_edges = clip_screen(edges)

    line_segments = edge_tracking(cropped_edges)
    line_segment_img = display_lines(img, line_segments)
    show_img("line segments", line_segment_img)

    lane_lines = lane_slope(img, line_segments)
    lane_lines_img = display_lines(img, lane_lines)

    return lane_lines, lane_lines_img

def clip_screen(canny):
    h, w = canny.shape 
    mask = np.zeros_like(canny)

    # only take the bottom half of the screen where lanes are visible
    poly = np.array([[
        (0, h * 1 / 2),
        (w, h * 1 / 2),
        (w, h),
        (0, h)
    ]], np.int32)

    # apply mask
    cv2.fillPoly(mask, poly, 255)
    show_img("mask", mask)
    cropped_edges = cv2.bitwise_and(canny, mask)
    
    show_img("edges clipped", cropped_edges)
    return cropped_edges

def detect_edges(img):
    # filter out white lines
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    show_img("hsv", hsv)

    # threshold for counting a pixel as white
    sensitivity = 30
    lower_white = np.array([0, 0, 147])
    upper_white = np.array([34, 118, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)

    # detect edges
    edges = cv2.Canny(mask, 200, 400)
    show_img("edges", edges)
    matplotlib.image.imsave("canny_result.png", edges)
    
    return edges

def edge_tracking(cropped_edges):
    precision = 1 # 1 pixel
    theta = np.pi / 180 # 1 degree
    min_threshold = 10
    line_segments = cv2.HoughLinesP(cropped_edges, precision, theta, min_threshold, np.array([]), minLineLength=8, maxLineGap=4)

    return line_segments

def lane_slope(img, line_segments):
    lane_lines = []

    # no lanes found
    if line_segments is None:
        return lane_lines

    h, w, _ = img.shape
    left = []
    right = []

    boundary = 1/3
    left_lane_boundary = w * (1 - boundary) # left lane on left 2/3 of screen (perspective)
    right_lane_boundary = h * boundary

    for segment in line_segments:
        for x1, y1, x2, y2 in segment:
            fit = np.polyfit((x1, x2), (y1, y2), 1) # y = mx + b
            m = fit[0]
            b = fit[1]
            if m < 0: # left lane
                if x1 < left_lane_boundary and x2 < left_lane_boundary:
                    left.append((m, b))
            else: # right lane
                if x1 > right_lane_boundary and x2 > right_lane_boundary:
                    right.append((m, b))

            left_avg = np.average(left, axis=0)
            if len(left) > 0:
                lane_lines.append(make_points(img, left_avg))
            
            right_avg = np.average(right, axis=0)
            if len(right) > 0:
                lane_lines.append(make_points(img, right_avg))

                return lane_lines


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# Helper Functions                                                                              #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

def display_lines(img, lines, line_color=(0, 255, 0), line_width=10):
    line_img = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), line_color, line_width)
    line_img = cv2.addWeighted(img, 0.8, line_img, 1, 1)
    return line_img

def display_heading_line(img, steering_angle, line_color=(0, 0, 255), line_width=5, ):
    heading_img = np.zeros_like(img)
    height, width, _ = img.shape

    # figure out the heading line from steering angle
    # heading line (x1,y1) is always center bottom of the screen
    # (x2, y2) requires a bit of trigonometry

    # Note: the steering angle of:
    # 0-89 degree: turn left
    # 90 degree: going straight
    # 91-180 degree: turn right
    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)

    cv2.line(heading_img, (x1, y1), (x2, y2), line_color, line_width)
    heading_img = cv2.addWeighted(img, 0.8, heading_img, 1, 1)

    return heading_img

def length_of_line_segment(line):
    x1, y1, x2, y2 = line
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def show_img(title, img, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, img)


def make_points(img, line):
    height, width, _ = img.shape
    slope, intercept = line
    y1 = height  # bottom of the img
    y2 = int(y1 * 1 / 2)  # make points from middle of the img down

    # bound the coordinates within the img
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def test_photo(file):
    my_follower = Follower()
    img = cv2.imread(file)
    combo_img = my_follower.follow(img)
    show_img('final', combo_img, True)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def compute_steering_angle(img, lane_lines):
    """ Find the steering angle based on lane line coordinate
        We assume that camera is calibrated to point to dead center
    """
    if len(lane_lines) == 0:
        return -90

    h, w, _ = img.shape
    if len(lane_lines) == 1: # follow lane detected
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
    else:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        camera_mid_offset_percent = 0.02 # 0.0 means car pointing to center, -0.03: car is centered to left, +0.03 means car pointing to right
        mid = int(w / 2 * (1 + camera_mid_offset_percent))
        x_offset = (left_x2 + right_x2) / 2 - mid

    # find the steering angle, which is angle between navigation direction to end of center line
    y_offset = int(h / 2)

    angle_to_mid_radian = math.atan(x_offset / y_offset)  # angle (in radian) to center vertical line
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
    steering_angle = angle_to_mid_deg + 90  # this is the steering angle needed by picar front wheel

    return steering_angle

def stabilize_steering_angle(curr_steering_angle, new_steering_angle, num_of_lane_lines, max_angle_deviation_two_lines=5, max_angle_deviation_one_lane=1):
    """
    Using last steering angle to stabilize the steering angle
    This can be improved to use last N angles, etc
    if new angle is too different from current angle, only turn by max_angle_deviation degrees
    """
    if num_of_lane_lines == 2 :
        # if both lane lines detected, then we can deviate more
        max_angle_deviation = max_angle_deviation_two_lines
    else :
        # if only one lane detected, don't deviate too much
        max_angle_deviation = max_angle_deviation_one_lane
    
    angle_deviation = new_steering_angle - curr_steering_angle
    if abs(angle_deviation) > max_angle_deviation:
        stabilized_steering_angle = int(curr_steering_angle
                                        + max_angle_deviation * angle_deviation / abs(angle_deviation))
    else:
        stabilized_steering_angle = new_steering_angle

    return stabilized_steering_angle


if __name__ == "__main__":
    f = "../test_data/center_lane.jpg"
    print(f"testing {f}")
    test_photo(f)