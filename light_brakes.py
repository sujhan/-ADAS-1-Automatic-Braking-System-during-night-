import cv2
import numpy as np
import time
 
cap = cv2.VideoCapture(1)
while True:
    ret,frame=cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)
    hi, threshold = cv2.threshold(blur, maxVal-20, 230, cv2.THRESH_BINARY)
    thr = threshold.copy()
    cv2.resize(thr, (300,300))
    edged = cv2.Canny(threshold, 50, 150)
    lightcontours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    circles = cv2.HoughCircles(threshold, cv2.cv.CV_HOUGH_GRADIENT, 1.0, 20,
                           param1=10,
                           param2= 15,
                           minRadius=20,
                           maxRadius=100,)
    if len(lightcontours)>0 and circles is not None:
        maxcontour = max(lightcontours, key=cv2.contourArea)
        if cv2.contourArea(maxcontour) > 50:
            (x, final_y), radius = cv2.minEnclosingCircle(maxcontour)
            cv2.circle(frame, (int(x), int(final_y)), int(radius), (0, 255, 0), 4)
            cv2.rectangle(frame, (int(x) - 5, int(final_y) - 5), (int(x) + 5, int(final_y) + 5), (0, 128, 255), -1)
            print("breaks applied")
    cv2.imshow('light', thr)
    cv2.imshow('frame', frame)
    cv2.waitKey(4)
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
