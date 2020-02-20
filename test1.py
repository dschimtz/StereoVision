import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# This is a test script using the phone camera.

rad_per_px = 0.0004861
resX = 4032
resY = 3024

# Image Data:
camX1 = 2621
camX2 = 548

camY1 = 2261
camY2 = 2262

pX1 = resX/2 - camX1
pX2 = resX/2 - camX2

pY1 = -resY/2 + camY1
pY2 = -resY/2 + camY2

phi1 = pX1*rad_per_px  + np.pi/2
phi2 = pX2*rad_per_px  + np.pi/2

theta1 = pY1*rad_per_px + np.pi/2
theta2 = pY2*rad_per_px + np.pi/2

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

r0 = 1
t0 = 1

x0 = np.array([r0,t0])

params = np.array([0.355])

res = sp.optimize.minimize(epsilon,x0,args=(phi1,phi2,theta1,theta2,params))

r = np.linspace(0,1.0,101)
t = np.linspace(0,1.0,101)

rayR,rayT = rays(r,t,phi1,phi2,theta1,theta2,params)

# results

fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
ax.plot(rayR[:,0],rayR[:,1],rayR[:,2])
ax.plot(rayT[:,0],rayT[:,1],rayT[:,2])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.legend(['cam1','cam2'])
ax.axis('equal')
error = res.fun
x_result = res.x

pos = rays(np.array([x_result[0]]),np.array([x_result[1]]),phi1,phi2,theta1,theta2,params)
pos1 = pos[0].copy()
pos2 = pos[1].copy()

