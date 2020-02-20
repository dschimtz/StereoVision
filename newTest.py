from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

vs = VideoStream(src=0).start()
tracker = cv2.Tracker("KCF")
time.sleep(2.0)
initBB = None
success = False
while True:
    frame = vs.read()

    frame = frame[1]

    if frame is None:
        break

    #frame = imutils.resize(frame, width=600)
    if initBB is not None:
            # grab the new bounding box coordinates of the object
            (success, box) = tracker.update(frame)
            
    if success:
            (x, y, w, h) = [int(v) for v in box1]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
            showCrosshair=True)

        tracker.init(frame, initBB)
