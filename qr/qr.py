
'''
Purpose: decode a QR code in a given image

Steps:

* detect corners
    * divide image into blocks and then look for similar frequencies
    * flood with liquid and find "moats"
    * "pattern matching" - sacle invariant?
    * corner detection: harris, eigenvalue
    * line detectoin
    * Hough Transform
    * Find contours with holes
* apply perspective transform
* read data
* error correction
'''

import Image
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import cv2
import os
import sys
import random
from sklearn.cluster import KMeans

def eq(x,y):
    return abs(x - y) < 0.000001

def to_gray(img):
    '''Returns the greyscale version of an image by simply summing pixels

    Coefficients taken from openCV's implementation
    (I don't know how they were chosen)
    '''

    return 0.299 * img[:, :, 0] + 0.587 * img[:, :, 0] + 0.114 * img[:, :, 0]

def get_threshold(img):
    hist = np.zeros((256))
    values = img.flatten().astype('int')
    for x in values:
        hist[int(x)] += 1.
    hist = hist / values.size

    assert eq(np.sum(hist), 1)
    p0 = 0.0
    p1 = 1.0
    mean = np.mean(values)
    mean0 = 0.0
    mean1 = mean
    max_var_btw = 0
    best_threshold = -1
    min_value = np.min(values)
    max_value = np.max(values)

    # The last pt cannot be a good threshold
    # (and it results in a tiny float which creates floating pt errors)
    # for threshold, prob in enumerate(hist[:-1]):
    for threshold in range(min_value, max_value):
        prob = hist[threshold]
        # if not eq(p0 + prob, 0) and not eq(p1 - prob, 0):
        mean0 = (p0 * mean0 + threshold * prob) / (p0 + prob)
        mean1 = (p1 * mean1 - threshold * prob) / (p1 - prob)
        p0 += prob
        p1 -= prob
        # print mean0, threshold, mean1, min_value, max_value
        # assert mean0 <= threshold <= mean1
        assert eq(1, p0 + p1)
        assert eq(p0 * mean0 + p1 * mean1, mean)
        var_btw = p0 * p1 * (mean1 - mean0) ** 2
        if var_btw > max_var_btw:
            max_var_btw = var_btw
            best_threshold = threshold

    return best_threshold



def binarize(img):
    '''Converts the given grayscale image to binary using the threshold
    calculated using Otsu's method

    '''
    threshold = get_threshold(img)
    print 'threshold:', threshold
    mask = img > threshold
    return mask.astype('int')

def get_image(filename):
    return np.asarray(Image.open(filename)).astype('uint8')

def get_corners(img):
    '''Finds all FinderPatterns using the algorithm specified
    in ISO/IEC 18004:

    1. Scan rows for sequence of 1:1:3:1:1 (b:w:b:w:b)
    2. For each match, check if the same sequence is found in the
    corresponding column

    Input image must be binary
    '''
    row_matches = [] # list of (r,start, end) tuples
    for i, row in enumerate(img):
        for start, end in get_pattern_in_vec(row):
            row_matches.append((i, start, end))
    col_matches = []
    for j, col in enumerate(img.T):
        for start, end in get_pattern_in_vec(col):
            col_matches.append((j, start, end))

    ratio_error = 2
    matches = []
    # Find all intersections of similar length lines
    for i, col_start, col_end in row_matches:
        for j, row_start, row_end in col_matches:
            row_length = row_end - row_start
            col_length = col_end - col_start
            if col_start + 2./7 * col_length < j < col_end - 2./7 * col_length and  \
                row_start + 2./7 * row_length < i < row_end - 2./7 * row_length:
                ratio = (col_end - col_start) / (row_end - row_start)
                if 1. / ratio_error < ratio < ratio_error:
                    matches.append((row_start, row_end, col_start, col_end))

    return matches

def get_pattern_in_vec(vec):
    vec_matches = []
    ratio_error = 1.5
    state = 0
    match = [-1, -1, -1, -1, -1]
    j = 0
    while j < len(vec):
        cell = vec[j]
        # print 'State: %d; Col: %d; Match: %s' % (state, j, match)
        if state == 0:
            # not started
            if cell == 0:
                state = 1
                match[0] = j
        elif state == 1:
            # in first black block
            if cell == 1:
                state = 2
                match[1] = j
        elif state == 2:
            # in first white block
            if cell == 0:
                # check if ratio is ~1:1
                ratio = float(j - match[1]) / (match[1] - match[0])
                if 1. / ratio_error < ratio < ratio_error:
                    state = 3
                    match[2] = j
                else:
                    state = 1
                    match = [j, -1, -1, -1, -1]
        elif state == 3:
            # in middle black block
            if cell == 1:
                # check if ratio is ~3
                # todo: also check ratio wrt first block?
                ratio = float(j - match[2]) / (match[2] - match[1])
                if 3. / ratio_error < ratio < 3 * ratio_error:
                    state = 4
                    match[3] = j
                else:
                    state = 1
                    match = [match[2], -1, -1, -1, -1]
        elif state == 4:
            # in second white block
            if cell == 0:
                ratio = float(j - match[3]) / (match[2] - match[1])
                if 1. / ratio_error < ratio < ratio_error:
                    state = 5
                    match[4] = j
                else:
                    state = 1
                    match = [match[2], -1, -1, -1, -1]
        elif state == 5:
            # in last black block
            if cell == 1:
                ratio = float(j - match[4]) / (match[4] - match[3])
                if 1. / ratio_error < ratio < ratio_error:
                    # found a match!
                    vec_matches.append((match[0], j))
                    state = 1
                    match = [match[4], -1, -1, -1, -1, -1]
        j += 1
    return vec_matches


def match_center(row_start, row_end, col_start, col_end):
    return ((row_end - row_start) / 2., (col_end - col_start) / 2.)

def dist((x0, y0), (x1, y1)):
    return (x1 - x0)**2 + (y1 - y0)**2

# def get_match_filter(img):
#     def match_filter(match):
#         rs, re, cs, ce = match
#         match_width = ce - cs
#         match_height = re - rs
#         small_square = img[rs + 2./7*match_width]

def check_match(match, bw_img):
    rs, re, cs, ce = match
    w = ce - cs
    h = re - rs
    c_rs = rs + int(2./7*h)
    c_re = re - int(2./7*h)
    c_cs = cs + int(2./7*w)
    c_ce = ce - int(2./7*w)
    s = np.sum(bw_img[c_rs:c_re, c_cs:c_ce])
    mean = float(s) / ((c_re - c_rs) * (c_ce - c_cs))
    return mean
    # bw_img[c_rs:c_re, c_cs:c_ce] = 2
    # plt.imshow(bw_img)
    # plt.show()


if __name__ == '__main__':
    # 1517 -> 1928
    img_filter = lambda s: s.lower().endswith('.jpg')
    for filename in filter(img_filter, os.listdir('dataset'))[:50]:
    # for filename in ['IMG_1522.JPG']:
        # print filename
        img = get_image('dataset/' + filename)
        img = gaussian_filter(img, sigma=1)
        gray = to_gray(img)
        bw_img = binarize(gray)
        # plt.imshow(bw_img)
        # plt.show()
        matches = get_corners(bw_img)
        print 'Found %d matches' % len(matches)
        vec = []
        display = bw_img.copy()
        for m in matches:
            rs, re, cs, ce = m
            display[rs:re, cs:ce] = 2
            vec.append(check_match(m, bw_img))
        plt.imshow(display)
        plt.show()
        plt.hist(vec, bins=50)
        plt.show()
        # vec = []
        # for rs, re, cs, ce in matches:
        #     bw_img[rs:re, cs:ce] = 2
        #     vec.append(s)
        # plt.imshow(bw_img)
        # plt.show()
        # print 'Sums:', vec
        # raw_input('[enter]')

        # good_matches = filter_matches(matches, gray.shape)
        # for rs, re, cs, ce in matches:
        #     bw_img[rs:re, cs:ce] = 2
        # plt.imshow(bw_img)
        # plt.show()

    # contours, hierachy = cv2.findContours(bw_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print 'found %d contours' % len(contours)
    # sizes = [c.size for c in contours]
    # plt.hist(sizes, bins=50)
    # plt.show()
    # red = cv2.cv.CV_RGB(255,0,0)
    # cv2.drawContours(bw_img, contours, -1, red, 2)
    # plt.imshow(bw_img)
    # plt.show()
    #
    # # corner_map = cv2.cornerHarris(bw_img, 2, 3, 0.04)
    #
    # plt.imshow(corner_map)
    # plt.show()
    # print get_pattern_in_row(row)
