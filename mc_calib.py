import numpy as np
from px_2_xyz import px_2_xyz
from Camera import Camera
import scipy as sp
import matplotlib.pyplot as plt

# This is the calibration script...it takes in some calibration data,
# and a ``camera'' object, and changes the camera object to update the 
# calibration. The calibration data is made up of 

def cost_function(params,calibData):
	
	X1 = calibData[0]
	Y1 = calibData[1]
	X2 = calibData[2]
	Y2 = calibData[3]
	
	pos_x = calibData[4]
	pos_y = calibData[5]
	pos_z = calibData[6]
	
	rad_per_px1 = params[0]
	rad_per_px2 = params[1]
	s = params[2]
	x_offset = params[3]
	z_offset = params[4]
	
	cam = Camera('samsungs7','samsungs7',1)
	
	cam.s = s
	cam.rad_per_px1 = rad_per_px1
	cam.rad_per_px2 = rad_per_px2
	
	result = px_2_xyz(X1,Y1,X2,Y2,cam,x_offset=x_offset,z_offset=z_offset)
	
	pos_predicted = result[0]
	
	pos_x_p = pos_predicted[0,0]
	pos_y_p = pos_predicted[0,1]
	pos_z_p = pos_predicted[0,2]
	
	return (pos_x_p - pos_x)**2 + (pos_y_p - pos_y)**2 + (pos_z_p - pos_z)**2 + 3*result[1]


def test_calib():
	
	camX1 = 2621
	camX2 = 548
	
	camY1 = 2261
	camY2 = 2262
	
	known_x = 0.095
	known_y = 0.535
	known_z = 0.103
	
	calibData = [camX1,camY1,camX2,camY2,known_x,known_y,known_z]
	
	params0 = [0.0004861,0.0004861,0.355,0.01,0.01]
	
	bounds = [(0.0004861,0.0004862),(0.0004861,0.0004862),(0.355,0.356),(-1,1),(-1,1)]
	
	result = sp.optimize.minimize(cost_function,params0,args=calibData,bounds=bounds)
		
	return result

def worst_case_calib():
	
	camX1 = 2621
	camX2 = 548
	
	camY1 = 2261
	camY2 = 2262
	
	known_x = 0.095
	known_y = 0.535
	known_z = 0.103
	
	calibData = [camX1,camY1,camX2,camY2,known_x,known_y,known_z]
	
	param1 = np.linspace(-0.3,0.3,41)
	param2 = np.linspace(-0.1,0.1,41)
	
	costMap = np.zeros([len(param1),len(param2)])
	
	for i in range(0,len(param1)):
		print(i)
		for j in range(0,len(param2)):
			
			params = [0.0004861,0.0004861,0.355,param1[i],param2[j]]
			
			costMap[i,j] = cost_function(params,calibData)

	plt.pcolor(param2,param1,np.log(costMap))

	return costMap
			

def mc_calib(cam,data):
	pass
	
#cost = worst_case_calib()

