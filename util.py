import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

def epsilon(x0,phi1,phi2,theta1,theta2,params):
	s = params[0]
	
	r = x0[0]
	t = x0[1]
	
	a = np.sin(theta1) * np.cos(phi1)
	b = np.sin(theta2) * np.cos(phi2)
	c = s
	
	d = np.sin(theta1) * np.sin(phi1)
	e = np.sin(theta2) * np.sin(phi2)
	
	f = np.cos(theta1)
	g = np.cos(theta2)
	
	return np.sqrt( (a*r - b*t - c)**2 + (d*r - e*t)**2 + (f*r - g*t)**2 )

def rays(r,t,phi1,phi2,theta1,theta2,params):
	s = params[0]

	a = np.sin(theta1) * np.cos(phi1)
	b = np.sin(theta2) * np.cos(phi2)
	c = s
	
	d = np.sin(theta1) * np.sin(phi1)
	e = np.sin(theta2) * np.sin(phi2)
	
	f = np.cos(theta1)
	g = np.cos(theta2)

	rayR_x = a*r
	rayR_y = d*r
	rayR_z = f*r
	
	rayT_x = b*t + c
	rayT_y = e*t
	rayT_z = g*t
	
	rayR = np.zeros([len(r),3])
	rayT = np.zeros([len(t),3])
	
	rayR[:,0] = rayR_x
	rayR[:,1] = rayR_y
	rayR[:,2] = rayR_z
	
	rayT[:,0] = rayT_x
	rayT[:,1] = rayT_y
	rayT[:,2] = rayT_z
	
	return rayR, rayT

def equal_plot(X,Y,Z,ax):

		ax.plot(X,Y,Z,'o-')
		
		max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
		Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
		Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
		Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
		# Comment or uncomment following both lines to test the fake bounding box:
		for xb, yb, zb in zip(Xb, Yb, Zb):
		   ax.plot([xb], [yb], [zb], 'w')

def plot_rays(r,t,phi1,phi2,theta1,theta2,params):
	
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	
	rayR, rayT = rays(r,t,phi1,phi2,theta1,theta2,params)

	X = rayR[:,0]
	Y = rayR[:,1]
	Z = rayR[:,2]
	equal_plot(X,Y,Z,ax)
	
	X = rayT[:,0]
	Y = rayT[:,1]
	Z = rayT[:,2]
	equal_plot(X,Y,Z,ax)
	
	return ax

	
	
	
	
	
	