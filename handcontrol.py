import cv2
import numpy
import handtracking

wCam, hCam = 1208, 720

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(3, wCam)
capture.set(4, hCam)

detector = handtracking.HandDetector(complexity=0, detect_confidence=0.7)

while True:
    success, image = capture.read()

    image = detector.find_hands(image)
    landmark_list = detector.find_position(image, draw=False)
    if len(landmark_list) != 0:
        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[8][1], landmark_list[8][2]

        cv2.circle(image, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(image, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(image, ((x1+x2)//2, (y1+y2)//2),
                   10, (255, 0, 255), cv2.FILLED)

        length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        
        if length < 50:
            cv2.circle(image, ((x1+x2)//2, (y1+y2)//2),
                   10, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Image", image)
    cv2.waitKey(1)
