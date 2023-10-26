import numpy as p
import cv2 as cv

# https://github.com/leswright1977/PySpectrometer/issues/27 add cv.CAP_V4L,
# also see https://forums.raspberrypi.com/viewtopic.php?t=331441
cap = cv.VideoCapture(0,  cv.CAP_V4L)
if not cap.isOpened():
    print("Cannot open Camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    cv.imshow('frame', gray)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
