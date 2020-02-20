import numpy as np
import scipy as sp
from Camera import Camera
from util import epsilon,rays,plot_rays
from scipy import optimize

# This code takes pixel data (from wherever, opevCV, hand-taken data) and 
# gives the coordinates that you want.

# A couple things:

# 1) You need to input X1,Y1 (the pixel coords from camera 1), X2,Y2 (from 
# camera 2) AND a ''camera object'' - this contains all the necessary calibrated
# data about the relative positions of the cameras, the relative orientations,
# the field of view of the cameras, the framerate....etc

# 2) you can input more than one set of input data at a time...that means
# you can track multiple objects at a time...to do this, input data like this:


#  [#,#,#.....#,#,#]  --> each column is its own object
#  [#,#,#.....#,#,#]
#  [#,#,#.....#,#,#]
#       .....
#
#    and each row represents one instant in time
    

def px_2_xyz(x1,y1,x2,y2,cam,isPlotting=False):
	
	# Image Data:
	camX1 = x1
	camX2 = x2
	
	camY1 = y1
	camY2 = y2
	
	pX1 = cam.resX1/2 - camX1
	pX2 = cam.resX2/2 - camX2 + cam.x_offset
	
	pY1 = -cam.resY1/2 + camY1
	pY2 = -cam.resY2/2 + camY2 - cam.z_offset
	
	phi1 = pX1*cam.rad_per_px1  + np.pi/2
	phi2 = pX2*cam.rad_per_px2  + np.pi/2
	
	theta1 = pY1*cam.rad_per_px1 + np.pi/2
	theta2 = pY2*cam.rad_per_px2 + np.pi/2
	
	r0 = 1
	t0 = 1
	
	x0 = np.array([r0,t0])
	
	params = np.array([cam.s])
	
	res = sp.optimize.minimize(epsilon,x0,args=(phi1,phi2,theta1,theta2,params))
	
	error = res.fun
	x_result = res.x
	
	pos = rays(np.array([x_result[0]]),np.array([x_result[1]]),phi1,phi2,theta1,theta2,params)
	pos1 = pos[0].copy()
	pos2 = pos[1].copy()
	
	result = (pos1+pos2)/2 # take the average of the two estimated positions
	
	if (error > 0.1*np.linalg.norm(result)):
		result[0,0] = np.nan
		result[0,1] = np.nan
		result[0,2] = np.nan
		
	if (result[0,1] < 0):
		result[0,0] = np.nan
		result[0,1] = np.nan
		result[0,2] = np.nan
	
	output = [result,error]
	
	#doing some plotting
	if (isPlotting == True):
		r = np.linspace(0,1,101)
		t = np.linspace(0,1,101)
		
		ax = plot_rays(r,t,phi1,phi2,theta1,theta2,params)
		ax.scatter(result[0,0],result[0,1],result[0,2])
		
	 
	return output

def testrun():
	cam = Camera('samsungs7','samsungs7',0.355)
	camX1 = 2621
	camX2 = 548
	
	camY1 = 2261
	camY2 = 2262
	px_2_xyz(camX1,camY1,camX2,camY2,cam,isPlotting=True,x_offset=0.0,z_offset=-0.0)
	
#testrun()
		
