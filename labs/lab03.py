import numpy as np 
import cv2



if __name__ == "__main__":
    #print(cv2.__version__)
    high_detail = cv2.imread(r"../data/HighDetailImage.tif")
    low_detail = cv2.imread(r"../data/LowDetailImage.tif")
    cv2.resize(high_detail, dsize=(10,10))