import cv2
import random
import time

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW
count = 0

number_boxes = int(input('Numarul dorit de cutii: '))
creat = 0
while True:

    success, image = capture.read()

    if time.time() - creat > 5:
        box_coord = []
        image_height, image_width = image.shape[0], image.shape[1]
        for i in range(number_boxes):
            width = random.randrange(100, 200)
            height = int(width*1.3)
            x = random.randrange(0, image_width-width)
            y = random.randrange(0, image_height-height)
            coord = (x, y, width, height)
            print(f'Coordonate: {coord[0]}, {coord[1]}; Dimensiuni: {coord[2]}, {coord[3]}')
            box_coord.append(coord)
            creat = time.time()
        ok = True
        count += 1
        schimbat = True

    for i in range(number_boxes):
        if schimbat:
            print(
                f'Tura: {count}; Cutia: {i}; Coordonate: {box_coord[i][0]}, {box_coord[i][1]}; Dimensiuni: {box_coord[i][2]}, {box_coord[i][3]}')
            
        cv2.rectangle(image, (box_coord[i][0], box_coord[i][1]),
                      (x+box_coord[i][2], y+box_coord[i][3]), (255, 0, 255), 5)
    schimbat = False
    cv2.imshow("Image", image)
    cv2.waitKey(1)
