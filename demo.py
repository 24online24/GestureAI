import numpy as np
import mediapipe as mp
import tensorflow as tf
import webbrowser
import time
import cv2

def main():
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils

    # pune calea absolută, cea relativă nu merge
    model = tf.keras.models.load_model('D:/Codes_Scripts/ProiectAI/mp_hand_gesture')

    f = open('D:/Codes_Scripts/ProiectAI/gesture.names', 'r')

    classNames = f.read().split('\n')
    f.close()
    # print(classNames)

    cap = cv2.VideoCapture(0)
    first = False

    prev_time, curr_time = 0, 0

    while True:
        _, frame = cap.read()

        x, y, c = frame.shape

        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(framergb)

        className = ''

        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # print(lm.x, lm.y)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                prediction = model.predict([landmarks])

                classID = np.argmax(prediction)
                className = classNames[classID]

        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                       1, (0,0,255), 2, cv2.LINE_AA)

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        cv2.putText(frame, str(int(fps)), (600, 30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow("Output", frame)

        if className == 'fist' and first == False:
            first = True
            # path = '/usr/bin/vivaldi-stable' + ' %s' # calea absolută a browser-ului
            # webbrowser.get(path).open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', new = 1, autoraise = True)
        elif className == 'okay' and first == True:
            break

        if cv2.waitKey(1) == ord('q'): # tasta q pentru a închide
            break

    cap.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
