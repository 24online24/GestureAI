from distutils.util import execute
import cv2
import handtracking
import webbrowser
import time

wCam, hCam = 1208, 720

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(3, wCam)
capture.set(4, hCam)

detector = handtracking.HandDetector(complexity=0)
savedtime = time.time()
previous_time = 0
current_time = 0
while True:
    success, image = capture.read()

    image = detector.find_hands(image)
    landmark_list = detector.find_position(image, draw=False)
    if len(landmark_list) != 0:
        x = []
        y = []
        sumx = 0
        sumy = 0
        for i in range(1, 6):
            landmarkx = landmark_list[i*4][1]
            landmarky = landmark_list[i*4][2]
            x.append(landmarkx)
            y.append(landmarky)
            sumx += landmarkx
            sumy += landmarky
            cv2.circle(image, (landmarkx, landmarky),
                       8, (255, 0, 255), cv2.FILLED)

        x_center = sumx // 5
        y_center = sumy // 5
        cv2.circle(image, (x_center, y_center),
                   10, (255, 0, 255), cv2.FILLED)

        distances = []

        for i in range(5):
            cv2.line(image, (x[i], y[i]),
                     (x_center, y_center), (255, 0, 255), 3)
            distances.append(
                ((x[i] - x_center)**2 + (y[i] - y_center)**2)**0.5)

        execute = True
        for element in distances:
            if element > 50:
                execute = False

        if execute:
            cv2.circle(image, (x_center, y_center),
                       10, (0, 255, 0), cv2.FILLED)
            if time.time() - savedtime > 10:
                webbrowser.open('https://www.youtube.com/watch?v=6Kp0T6T6Ujg', 1)
                savedtime = time.time()

    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    cv2.putText(image, str(int(fps)), (1200, 30),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(1)
