import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import Image
import math
import sys
import random
import os
import re
from ransac import ransac

def stitch(file1, file2, output_file=None):
	print output_file
	if not output_file:
		output_file = file1.split('.')[0] + file2
		output_file = re.sub('[^a-zA-Z\-\.]', '', output_file)
		print output_file
	img1 = cv2.imread(file1)
	img2 = cv2.imread(file2)

	print file1
	print file2
	i1 = Image.open(file1).convert("RGBA")
	i2 = Image.open(file2).convert("RGBA")
	w1, h1 = i1.size
	w2, h2 = i2.size

	# sift = cv2.SIFT()
	surf = cv2.SURF(400)
	# surf.upright = True
	# fast = cv2.FastFeatureDetector()
	# orb = cv2.ORB()
	# kp, des = surf.detectAndCompute(img, None)
	kp1, des1 = surf.detectAndCompute(img1, None)
	print 'kp1:', len(kp1)
	kp2, des2 = surf.detectAndCompute(img2, None)
	print 'kp2:', len(kp2)
	if len(kp1) < 50 or len(kp2) < 50:
		return
	# kp = fast.detect(img, None)
	# kp1, des1 = orb.detectAndCompute(img1, None)
	# kp2, des2 = orb.detectAndCompute(img2, None)
	# print('* Found %d keypoints' % len(kp))
	# test = cv2.drawKeypoints(img1, kp1, None, (255,0,0), 4)
	# plt.imshow(test)
	# plt.show()

	bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
	matches = bf.match(des1, des2)
	if len(matches) < 50:
		return
	print 'matches:', len(matches)
	cutoff = 100

	# x1 = []
	# x2 = []
	# y1 = []
	# y2 = []
	a = []
	b = []

	x = []
	y = []


	for m in sorted(matches, key=lambda x:x.distance)[:cutoff]:
		p1 = kp1[m.queryIdx].pt
		p2 = kp2[m.trainIdx].pt
		a.append([p1[0]-w1/2, p1[1]-h1/2, 1])
		b.append([p2[0]-w2/2, p2[1]-h2/2, 1])
		x.append(p2[0] - p1[0])
		y.append(p2[1] - p1[1])
	transform = find_transform(a, b)
	x_offset = transform[2,0]
	y_offset = transform[2,1]
	sxcos = transform[0,0]
	sxsin = transform[0,1]
	sysin = -1*transform[1,0]
	sycos = transform[1,1]
	avg_atan = .5*(sxsin / sxcos + sysin / sycos)
	angle = math.atan(avg_atan)
	# Don't use sxsin/sin because the angle is usually negligible,
	# so dividing a tiny number by another tiny number will
	# magnify error
	sx = sxcos / math.cos(angle)
	sy = sycos / math.cos(angle)
		

	print '* x offset:', x_offset
	print '* y offset:', y_offset
	print '* x scale:', sx
	print '* y scale:', sy
	print '* angle:', angle, angle*180/math.pi

	if sx < 0 or sy < 0 or sx > 2 or sy > 2:
		print '* Bad scale, quitting'
		return
	elif abs(angle*180/math.pi) > 30:
		print '* Angle too large, quitting'
		return
	# if angle*180/math.pi > 3:
	# 	print '* Error - angle too large (%f)' % (angle*180/math.pi)
	# 	return file1
	else:
		i2 = i2.resize((int(w2/sx), int(h2/sy)), Image.ANTIALIAS)
		print i2.size
		# i2.show()
		i2 = i2.rotate(angle*180/math.pi, expand=True)
		print i2.size
		# i2.show()
		w2, h2 = i2.size
		print 'w1:', w1
		print 'h1:', h1
		print 'w2:', w2
		print 'h2:', h2

		if x_offset >= 0 and y_offset >= 0:
			# Place i2 to the top left
			print '* case 1'
			dim = (.5*w2+max(.5*w2, .5*w1+x_offset), .5*h2+max(.5*h2, .5*h1+y_offset))
			offset1 = (.5*w2+x_offset-.5*w1, .5*h2+y_offset-.5*h1)
			offset2 = (0,0)
		elif x_offset < 0 and y_offset < 0:
			# Place i2 to the bottom right
			print '* case 2'
			x_offset = abs(x_offset)
			y_offset = abs(y_offset)
			dim = ((.5*w1+max(.5*w1, .5*w2+x_offset), .5*h1+max(.5*h1, .5*h2+y_offset)))
			offset1 = (0,0)
			offset2 = (.5*w1+x_offset-.5*w2, .5*h1+y_offset-.5*h2)
		elif x_offset >= 0 and y_offset < 0:
			# Place i2 to bottom left
			print '* case 3'
			y_offset = abs(y_offset)
			dim = (.5*w2+max(.5*w2, x_offset+.5*w1), .5*h1+max(.5*h1, y_offset+.5*h2))
			offset1 = (.5*w2+x_offset-.5*w1, 0)
			offset2 = (0, .5*h1+y_offset-.5*h2)
		elif x_offset < 0 and y_offset >= 0:
			# Place i2 to top right
			print '* case 4'
			x_offset = abs(x_offset)
			dim = (.5*w1+max(.5*w1, x_offset+.5*w2), .5*h2+max(.5*h2, y_offset+.5*h1))
			offset1 = (0, .5*h2+y_offset-.5*h1)
			offset2 = (.5*w1+x_offset-.5*w2, 0)

		dim = (int(dim[0]), int(dim[1]))
		offset1 = (int(offset1[0]), int(offset1[1]))
		offset2 = (int(offset2[0]), int(offset2[1]))
		print 'dim:', dim
		print 'offset1:', offset1
		print 'offset2:', offset2
		background = Image.new('RGBA', dim, (255,255,255,255))
		background.paste(i1, offset1, i1)
		background.paste(i2, offset2, i2)
		print '* Saving as', output_file
		background.save(output_file)
		# background.show()
		# i1.show()
		# i2.show()
		return output_file	

def median(l):
	return sorted(l)[len(l)/2]

def find_transform(a, b):
	'''Finds the transform matrix which takes a n x 3 matrix of 2d 
	points and scales, rotates, and translates into another n x 3
	matrix. Returns the following transformation matrix (s=scale, t=translate):
	[sx cos(theta),  sx sin(theta), 0]
	[-sy sin(theta), sy cos(theta), 0]
	[tx,             ty,            1]'''
	a = np.matrix(a)
	b = np.matrix(b)
	bad_x = (a.T*a).I*(a.T*b)
	x = ransac(a, b)
	# print x
	y = a*bad_x
	z = a*x
	# plt.plot(a[:,0], b[:,0], 'ro', a[:,0], y[:,0], 'bo', a[:,0], z[:,0], 'go')
	# plt.show()

	return x

def bulk_stitch(folder):
	try:
		i = int(folder.split('-')[-1])
		new_folder = ''.join(folder.split('-')[:-1]) + '-' + str(i+1)
	except:
		new_folder = folder + '-1'
	try:
		os.mkdir(new_folder)
	except:
		print '* Folder already exists'
	files = [f for f in os.listdir(folder) if f.lower().endswith('.png') or f.lower().endswith('.jpg')]
	print files
	print '%d images left to process' % len(files)
	print len(files)
	if len(files) > 1:
		if len(files) % 2 == 1:
			filename = files.pop(-1)
			f = open(folder + '/' + filename)
			open(new_folder+'/'+filename, 'wb').write(f.read())
		for c in range(0, len(files), 2):
			f1 = files[c]
			f2 = files[c+1]
			print 'Stitching', f1, f2
			stitch(folder+'/'+f1, folder+'/'+f2, new_folder+'/'+f1)
		bulk_stitch(new_folder)
	else:
		return files[0]

def bulk_stitch_2(folder, base=None):
	files = [f for f in os.listdir(folder) if f.lower().endswith('.png') or f.lower().endswith('.jpg')]
	if not base:
		base = files.pop(0)
	for f in files:
		print '* Stitching', f
		stitch(folder+'/'+base, folder+'/'+f, output_file=folder+'/'+base)


if __name__ == '__main__':
	# stitch('space/11.png', 'space/12.png', output_file = 'space-1/10.png')
	x = bulk_stitch_2('test2')
	# stitch('hood_half.jpg', 'hood_rot.jpg')
	# print type(x)
	# print x
	# bulk_stitch_2('river')
	# print f
	# start = time.time()
	# files = [f for f in os.listdir('.') if f.endswith('.png') or f.endswith('.jpg')][:5]
	# bulk_stitch(files)
	# print('* %f sec' % (time.time() - start))
	# stitch('boston/3.png', 'boston/6.png')



