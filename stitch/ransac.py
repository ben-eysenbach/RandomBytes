import random
import numpy as np
import matplotlib.pyplot as plt

def ransac(A, B, threshold=10, p=.4):
	'''Solves for the best x in Ax=B using the RANSAC algorithm'''
	max_correct = 0
	m, n = A.shape
	while max_correct < p:
		rows = random.sample(range(m), n)
		a = A[rows,:]
		b = B[rows,:]
		try:
			x = a.I * b
			error_matrix = B - A*x
			print 'error:', error_matrix.sum()
			good_cells = np.less(np.abs(error_matrix), threshold).sum()
			print 'good cells:', good_cells
			correct = 1.0 * good_cells / B.size
			if correct >= max_correct:
				best_x = x
				max_correct = correct
				print 'correct:', correct
				print 'Found new best x!'
		except:
			print 'Singular matrix, ignoring'
		threshold *= 1.01
	print threshold
	return best_x

if __name__ == '__main__':
	A = np.matrix(range(200)).T
	A.resize((50,4))
	B = []
	for k in range(200):
		if k % 2 == 0:
			B.append(k+random.random())
		else:
			B.append(200*random.random())
	B = np.matrix(B).T
	B.resize(50,4)
	x = ransac(A, B)
	# bad_x = (A.T*A).I*A.T*B
	# plt.plot(A, B, 'ro', A, A*x, 'g-')
	# plt.plot(A, B, 'ro', A, A*bad_x, 'b-', A, A*x, 'g-')
	# plt.show()

