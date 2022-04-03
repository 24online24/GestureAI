import cv2
import mediapipe
import time

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW

mediapipe_hands = mediapipe.solutions.hands
hands = mediapipe_hands.Hands()
mediapipe_draw = mediapipe.solutions.drawing_utils

previous_time = 0
current_time = 0

while True:
    success, image = capture.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    # print(results.multi_hand_landmarks)

    x4, y4, x8, y8 = 0, 0, 0, 0
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                # print(id, landmark)
                height, width, channel = image.shape
                x, y = int(landmark.x*width), int(landmark.y*height)
                #print(id, x, y)

                if id == 4:
                    x4, y4 = x, y
                elif id == 8:
                    x8, y8 = x, y
                result= ((((x8 - x4 )**2) + ((y8-y4)**2) )**0.5)
                print(result, end=' ')
                if result < 30:
                    print('near')
                elif 50 < result < 100:
                    print('medium')
                elif 120 < result:
                    print('far')

            mediapipe_draw.draw_landmarks(
                image, hand_landmarks, mediapipe_hands.HAND_CONNECTIONS)

    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    cv2.putText(image, str(int(fps)), (600, 30),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(1)
