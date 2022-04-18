import cv2
import random


capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW

ok = False

number_boxes = int(input())
box_coord = []

while True:
    success, image = capture.read()

    if not ok:
        image_height, image_width = image.shape[0], image.shape[1]
        for i in range(number_boxes):
            width = random.randrange(100, 200)
            height = int(width*1.3)
            x = random.randrange(0, image_width-width)
            y = random.randrange(0, image_height-height)
            clr = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            coord = (x, y, width, height, clr)
            print(coord)
            box_coord.append(coord)

        print(image_height, image_width)
        ok = True

    for i in range(number_boxes):
        cv2.rectangle(image, (box_coord[i][0], box_coord[i][1]),
                      (x+box_coord[i][2], y+box_coord[i][3]), box_coord[i][4], 5)
    cv2.imshow("Image", image)
    cv2.waitKey(1)
