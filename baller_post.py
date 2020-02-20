# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import threading
from px_2_xyz import px_2_xyz
from Camera import Camera
from pynput.keyboard import Key, Listener
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from util import equal_plot
import pandas as pd

class coordinatePoint():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camTrack(self.previewName, self.camID)

def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

def camTrack(previewName, camID):
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
    args = vars(ap.parse_args())

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    greenLower = (80, 80, 0)
    greenUpper = (100, 255, 255)
    pts = deque(maxlen=args["buffer"])

    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
        vs = VideoStream(src=camID).start()

    # otherwise, grab a reference to the video file
    else:
        vs = cv2.VideoCapture(args["video"])

    # allow the camera or video file to warm up
    time.sleep(2.0)

    # keep looping
    while True:
        # grab the current frame
        frame = vs.read()

        # handle the frame from VideoCapture or VideoStream
        frame = frame[1] if args.get("video", False) else frame

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if frame is None:
            break

        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if previewName == "Camera 1":
                coordinate1.x = x
                coordinate1.y = y
                #print("x1: %d y1: %d x2: " % (x1, y1))
            elif previewName == "Camera 2":
                coordinate2.x = x
                coordinate2.y = y
               # print("x2: %d y2: %d" % (x2, y2))
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # update the points queue
        pts.appendleft(center)

        # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the frame to our screen
        cv2.imshow(previewName, frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    # if we are not using a video file, stop the camera video stream
    if not args.get("video", False):
        vs.stop()

    # otherwise, release the camera
    else:
        vs.release()

    # close all windows
    cv2.destroyAllWindows()

global global_cam

global_cam = Camera("hacknc")
coordinate1 = coordinatePoint(0,0)
coordinate2 = coordinatePoint(0,0)

def main():
    # Collect events until released
    
    N = 101
	
    path = np.zeros([3,N])
	
	
    thread1 = camThread("Camera 1", 1)        
    thread2 = camThread("Camera 2", 2)
    thread1.start()
    time.sleep(1)
    thread2.start()
    time.sleep(3)
	
#    with Listener(on_press=on_press,on_release=on_release) as listener:
#        listener.join()
	
    for i in range(N):
        result = px_2_xyz(coordinate1.x, coordinate1.y, coordinate2.x, coordinate2.y, global_cam)
        coords = result[0]
#        print(coordinate1.x)
#        print(coordinate2.x)
#        print(coordinate1.y)
#        print(coordinate2.y) 
        print(result[0])
        
        time.sleep(0.1)
        path[0,i] = coords[0,0]
        path[1,i] = coords[0,1]
        path[2,i] = coords[0,2]
    csvpath = pd.DataFrame(path)
    print(csvpath)
    csvpath.to_csv('test')
		
    fig = plt.figure(1)
    fig.clf()
    ax = fig.gca(projection='3d')
    equal_plot(path[0,:],path[1,:],path[2,:],ax)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.scatter(0,0,0)
    ax.scatter(global_cam.s,0,0)
    

if __name__ == "__main__":
    main()