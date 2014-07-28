import cv2
from pymouse import PyMouse
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import uniform_filter

def control_mouse():

    m = PyMouse()
    screen_width, screen_height = m.screen_size()
    cap = cv2.VideoCapture(0)
    mouse_img = cv2.imread('key.jpg')
    # plt.imshow(mouse_img)
    # surf = cv2.SURF(400)
    # kp1, des1 = surf.detectAndCompute(mouse_img, None)
    # print 'Starting with %d kp' % len(kp1)
    red = cv2.cv.CV_RGB(255,0,0)
    while True:
        flag, frame = cap.read()
        # kp2, des2 = surf.detectAndCompute(frame, None)
        # print 'Got %d kp' % len(kp2)
        # bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        # matches = bf.match(des1, des2)

        # pt_list = []

        # for match in sorted(matches, key=lambda x:x.distance)[:10]:
            # pt_list.append(kp2[match.trainIdx].pt)
            # pt = tuple(map(int, kp2[match.trainIdx].pt))
            # cv2.circle(frame, pt, 5, red)

        # median_x = int(np.median([x for x,y in pt_list]))
        # median_y = int(np.median([y for x,y in pt_list]))
        # m.move(median_x, median_y)

        frame_width, frame_height, depth = frame.shape
        match = cv2.matchTemplate(mouse_img, frame, cv2.cv.CV_TM_CCORR)
        smoothed = uniform_filter(match, size=5)
        print 'S:', smoothed.shape
        print 'F:', frame.shape
        # new_frame = match.resize((frame_width, frame_height))
        max_index = np.argmin(match)
        max_index_row = max_index / frame_width
        max_index_col = max_index % frame_width

        red = cv2.cv.CV_RGB(255,0,0)
        cv2.circle(frame, (max_index_row, max_index_col), 50, red)
        # cv2.imshow('frame', smoothed)
        plt.imshow(match)
        plt.show()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    control_mouse()
