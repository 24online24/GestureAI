import cv2
import mediapipe
import time


class HandDetector():
    def __init__(self, static_image=False, max_hands=2, complexity=1, detect_confidence=0.5, track_confidence=0.5):
        self.static_image = static_image
        self.max_hands = max_hands
        self.complexity = complexity
        self.detect_confidence = detect_confidence
        self.track_confidence = track_confidence

        self.mediapipe_hands = mediapipe.solutions.hands
        self.hands = self.mediapipe_hands.Hands(
            self.static_image, self.max_hands, self.complexity, self.detect_confidence, self.track_confidence)
        self.mediapipe_draw = mediapipe.solutions.drawing_utils

    def find_hands(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mediapipe_draw.draw_landmarks(
                        image, hand_landmarks, self.mediapipe_hands.HAND_CONNECTIONS)
        return image

    def find_position(self, image, hand_number=0, draw=True):
        landmarks_list = []
        if self.results.multi_hand_landmarks:
            current_hand = self.results.multi_hand_landmarks[hand_number]
            for id, landmark in enumerate(current_hand.landmark):
                height, width, channel = image.shape
                x, y = int(landmark.x*width), int(landmark.y*height)
                landmarks_list.append([id, x, y])
                if draw:
                    cv2.circle(image, (x, y), 10, (255, 0, 255), cv2.FILLED)

        return landmarks_list


def main():
    previous_time = 0
    current_time = 0
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = HandDetector(complexity=1)
    while True:
        success, image = capture.read()
        image = detector.find_hands(image)
        landmarks_list = detector.find_position(image, draw=False)
        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time
        cv2.putText(image, str(int(fps)), (600, 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow("Image", image)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
