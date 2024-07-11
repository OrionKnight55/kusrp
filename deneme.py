import cv2
import numpy as np

def rotate_image(image, angle):
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_image
def horizontal_flip(image):
    return cv2.flip(image, 1)
image = cv2.imread('input1.jpg')
cv2.imshow('image',image)
cv2.waitKey(0)
#rotated_image = rotate_image(image, 135)
#cv2.imwrite('C:/Users/world/Downloads/kusrp/rotated.jpg', rotated_image)