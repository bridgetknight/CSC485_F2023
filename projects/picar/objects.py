
# UNFINISHED 

class Stimuli(stimuli):

    def set_car_state(self, car_state):
        pass

    def is_close(stim, img_height, min_height=0.05):
        # checking if a sign is 10% the height of the image
        stim_h = stim.bounding_box[1][1]-stim.bounding_box[0][1]
        return 