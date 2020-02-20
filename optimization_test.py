import scipy as sp
import numpy as np

def f(v):
	x = v[0]
	y = v[1]
	return (x+1)**2 + (y-2)**2


x0 = np.array([3,3])

res = sp.optimize.minimize(f,x0)
x_R = res.x