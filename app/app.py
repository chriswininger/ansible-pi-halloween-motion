import cv2
from adafruit_servokit import ServoKit
import datetime

IN_MIN = 30.0
IN_MAX = 160.0
OUT_MIN = 160.0
OUT_MAX = 30.0

def main():
    # State
    head_angle = 90.0
    head_angle_ave = 90.0
    head_angle_alpha = 0.25

    print('Running ', datetime.datetime.now())

    kit = ServoKit(channels=16)

    cap = cv2.VideoCapture(0, cv2.CAP_V4L)

    # from original skellington sketch (not sure I need to set it this low)
    cap.set(3, 160)  # set horiz resolution
    cap.set(4, 120)  # set vert res

    if not cap.isOpened():
        print("Cannot open Camera")
        exit()

    # threshold higher means it picks up fewer false positives, history takes into account past frames?
    object_detector = cv2.createBackgroundSubtractorMOG2(history=10, varThreshold=5)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break

        height, width, _ = frame.shape

        # only look at region of interest (roi)
        # here I'm setting to full resolution, but if there was only a portion
        # of screen that could have objects, could reduce this
        roi = frame[0: 240, 0: 320] # seems to be height range, width?
        mask = object_detector.apply(roi)

        # object detection
        # contours is each identified area, hierarchy tells you information about which is inside another
        # RETR_EXTERNAL only grabs the outer contours, not any inside other ones
        contours, hierarchy =cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        biggest_index = 0
        biggest_area = 0
        ind = 0
        for cnt in contours:
            #calc area and ignore small
            area = cv2.contourArea(cnt)
            if area > 150:
                #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                x,y,w,h = cv2.boundingRect(cnt)
                detections.append([x,y,w,h])
                area = w*h
                if area > biggest_area:
                    biggest_area = area
                    biggest_index = ind
                ind = ind + 1

        # draw rect around biggest contour
        #print(detections)
        if (len(detections) > 0):
            x,y,w,h = detections[biggest_index]
            cv2.rectangle(roi, (x,y), (x+w, y+h), (0, 255, 0), 3)
            #print('x: ' + str(x) + ', w: ' + str(w))
            head_angle = remap(float(x+(float(w)/2.0)), IN_MIN,IN_MAX,OUT_MIN,OUT_MAX)
            print('x: ' + str(x) + ', head: ' + str(head_angle))

        head_angle_ave = head_angle * head_angle_alpha + head_angle_ave * (1.0 - head_angle_alpha)

        # uncomment for debugging
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# map one range to another
def remap(x, in_min, in_max, out_min, out_max):

    x_diff = x - in_min

    out_range = out_max - out_min

    in_range = in_max - in_min
    temp_out = x_diff * out_range/in_range + out_min
    #print('x: ' + str(x) + ', temp_out: ' + str(temp_out))
    if out_max < out_min:
        temp = out_max
        out_max = out_min
        out_min = temp

    if temp_out > out_max:
        return out_max
    elif temp_out < out_min:
        return out_min
    else:
        return temp_out

if __name__ == "__main__":
    main()
