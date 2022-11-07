import cv2
import random
import hand_tracking
import time

import tkinter as tk
from tkinter import Menu
import tkinter.messagebox as ms

WIDTH = 640
HEIGHT = 480

global highscore, clicked, root, prev_score, _exit, file, file1


def create_box(image):
    image_height, image_width = image.shape[0], image.shape[1]
    box_width = random.randrange(WIDTH // 6, WIDTH // 4)
    box_height = int(box_width * 1.3)
    x = random.randrange(0, image_width - box_width)
    y = random.randrange(0, image_height - box_height)
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


def show_highscore():
    ms.showinfo("Highscore", f"Highscore = {highscore}")


def show_prev_score():
    global prev_score
    ms.showinfo("Previous Score", f'Previous Score = {prev_score}')


def onClick():
    global root, _exit
    _exit = True
    root.destroy()


def start_game():
    global clicked, root
    clicked = True
    root.destroy()


def place_buttons():
    global prev_score, highscore

    file = open("highscore.txt", 'r+')
    highscore = int(file.read())
    file1 = open("prev_score.txt", 'r+')
    prev_score = int(file1.read())

    b1 = tk.Button(root, text="Show Highscore", command=show_highscore)
    b2 = tk.Button(root, text="Show previous score", command=show_prev_score)
    b3 = tk.Button(root, text="Start game", command=start_game)

    b2.place(x=HEIGHT // 2 + 10, y=HEIGHT // 2 - HEIGHT // 3)
    b1.place(x=HEIGHT // 2 + 23, y=HEIGHT // 2 - HEIGHT // 4.5)
    b3.place(x=HEIGHT // 2 + 36, y=HEIGHT // 1.93 - HEIGHT // 8)


def menu():
    global root
    root = tk.Tk(className=" Gesture Game")

    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.after(1, place_buttons)
    root.protocol("WM_DELETE_WINDOW", onClick)
    root.mainloop()


def game():
    global highscore, prev_score, clicked, _exit

    file = open("highscore.txt", 'r+')
    file1 = open("prev_score.txt", 'r+')

    # capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capture = cv2.VideoCapture(2)


    capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    box_now = found = False
    first_box = True
    start_time = time.time()
    previous_time = start_time
    current_time = 0
    score = -1
    tracker = hand_tracking.HandDetector()
    timer = random.randint(12, 15)

    while True and clicked:
        success, image = capture.read()

        # if timer <= 0.1:
        #     if score > highscore:
        #         file.seek(0)
        #         file.truncate()
        #         file.writelines(str(score))

        #     file1.seek(0)
        #     file1.truncate()
        #     file1.writelines(str(score))

        #     break

        if box_now == False:
            score += 1
            coordinates = create_box(image)
            box_now = True
            found = False

            if first_box:
                first_box = not first_box
            else:
                timer = random.randint(7, 10)

        cv2.rectangle(image, (coordinates[0], coordinates[1]),
                      (coordinates[0] + coordinates[2], coordinates[1] + coordinates[3]), (255, 0, 255), 5)
        found = detect_hand(image, coordinates, tracker)
        box_now = not found

        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        cv2.putText(image, str(int(fps)), (WIDTH - 40, 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.rectangle(image, (0, 0), (125, 130), (128, 128, 128), -1)

        elapsed = round(current_time - start_time, 2)
        speed = round(score / elapsed, 2)

        cv2.putText(image, 'Highscore: ' + str(highscore), (10, 30),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        cv2.putText(image, 'Score: ' + str(score), (10, 60),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        cv2.putText(image, 'Time: ' + str(elapsed), (10, 90),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        cv2.putText(image, 'Timer: ' + str(round((timer := timer - 0.1), 2)), (10, 120),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        cv2.imshow("Image", image)
        cv2.waitKey(1)

        if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            _exit = True
            break

    cv2.destroyAllWindows()

    file.close()
    file1.close()


funcmap = {
    1: menu,
    2: game
}

if __name__ == '__main__':
    _exit = False

    choice = 1
    while True:
        choice = 1
        funcmap[choice]()

        if _exit:
            break

        choice = 2
        funcmap[choice]()

        if _exit:
            break
