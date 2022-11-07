import cv2

cam = cv2.VideoCapture(2)  # camera index (default = 0) (added based on Randyr's comment).

print('cam has image : %s' % cam.read()[0]) # True = got image captured. 
                                           # False = no pics for you to shoot at.

# Lets check start/open your cam!
if cam.read() == False:
    cam.open()

if not cam.isOpened():
    print('Cannot open camera')

while True:
    ret,frame = cam.read()
    cv2.imshow('webcam', frame)
    if cv2.waitKey(1)&0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()