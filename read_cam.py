"""
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.

TAKEN FROM ONLINE
"""

import cv2


def show_webcam(mirror=False):
    cam1 = cv2.VideoCapture(1)
    cam2 = cv2.VideoCapture(2)
    while True:
        ret1_val, img1 = cam1.read()
        ret2_val, img2 = cam2.read()
        if mirror: 
            img1 = cv2.flip(img1, 1)
            img2 = cv2.flip(img2, 1)
        cv2.imshow('my webcam1', img1)
        cv2.imshow('my webcam2', img2)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()