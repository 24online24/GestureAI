import cv2
import random

def create_box(image):
    image_height, image_width = image.shape[0], image.shape[1]
    width = random.randrange(100, 200)
    height = int(width*1.3)
    x = random.randrange(0, image_width-width)
    y = random.randrange(0, image_height-height)
    coord = (x, y, width, height)
    ok = True
    cv2.rectangle(image, (x, y),
                    (x+width, y+height), (255, 0, 255), 5)

#def detect_hand():


if __name__ == '__main__':
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW
    while True:
        success, image = capture.read()
        cv2.imshow("Image", image)
        cv2.waitKey(1)
