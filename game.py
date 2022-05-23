import cv2
import random
import HandTracking
import time


WIDTH = 640
HEIGHT = 480


def create_box(image):
    image_height, image_width = image.shape[0], image.shape[1]
    box_width = random.randrange(WIDTH//6, WIDTH//4)
    box_height = int(box_width*1.3)
    x = random.randrange(0, image_width-box_width)
    y = random.randrange(0, image_height-box_height)
    return((x, y, box_width, box_height))


def detect_hand(image, area, detector):
    image = detector.find_hands(image)
    landmarks = detector.find_position(image, draw=False)
    if not landmarks:
        return False

    for landmark in landmarks:
        if landmark[1] < area[0] or landmark[1] > area[0] + area[2] or landmark[2] < area[1] or landmark[2] > area[1] + area[3]:
            return False
    return True


if __name__ == '__main__':
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW
    mode = int(input('0 for 480p/ 1 for 1080p: '))
    if mode:
        WIDTH = 1920
        HEIGHT = 1080
    else:
        WIDTH = 640
        HEIGHT = 480
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    box_now = False
    found = False
    start_time = time.time()
    previous_time = start_time
    current_time = 0
    score = -1
    tracker = HandTracking.HandDetector()
    while True:
        success, image = capture.read()
        if box_now == False:
            score += 1
            coordinates = create_box(image)
            box_now = True
            found = False
        cv2.rectangle(image, (coordinates[0], coordinates[1]),
                      (coordinates[0]+coordinates[2], coordinates[1]+coordinates[3]), (255, 0, 255), 5)
        found = detect_hand(image, coordinates, tracker)
        # print(found)
        box_now = not found

        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time
        cv2.putText(image, str(int(fps)), (WIDTH - 40, 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.rectangle(image, (0, 0), (125, 100), (128, 128, 128), -1)

        elapsed = round(current_time-start_time, 2)
        speed = round(score/elapsed, 2)
        cv2.putText(image, 'Time: ' + str(elapsed), (10, 30),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        cv2.putText(image, 'Score: ' + str(score), (10, 60),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        cv2.putText(image, 'Speed: ' + str(speed), (10, 90),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        cv2.imshow("Image", image)
        cv2.waitKey(1)
