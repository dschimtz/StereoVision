import numpy as np
from px_2_xyz import px_2_xyz
from Camera import Camera
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

# This is the calibration script...it takes in some calibration data,
# and a ``camera'' object, and changes the camera object to update the 
# calibration. The calibration data is made up of 

def cost_function(params,calibData):
	
	cost = 0
	
	for i in range(0,len(calibData)):
		calibData_I = calibData[i]
	
		X1 = calibData_I[0]
		Y1 = calibData_I[1]
		X2 = calibData_I[2]
		Y2 = calibData_I[3]
		
		pos_x = calibData_I[4]
		pos_y = calibData_I[5]
		pos_z = calibData_I[6]
		
		rad_per_px1 = params[0]
		rad_per_px2 = params[1]
		
		cam = Camera('hacknc')
		
		cam.rad_per_px1 = rad_per_px1
		cam.rad_per_px2 = rad_per_px2
		
		result = px_2_xyz(X1,Y1,X2,Y2,cam)
		
		pos_predicted = result[0]
		
		pos_x_p = pos_predicted[0,0]
		pos_y_p = pos_predicted[0,1]
		pos_z_p = pos_predicted[0,2]
		
		#may leave out the x component since we don't know it very well during calibration
		cost = cost + (pos_x_p - pos_x)**2 + (pos_y_p - pos_y)**2 + 3*result[1]
	return cost
		
		
def calibration():
	
	calibData1 = [294.5, 190.5,  16.5, 185.5, 0, 3.6576,0]
	calibData2 = [296.0, 192.0,  72.5, 187.5, 0, 4.572,0]
	calibData3 = [400.0, 193.0, 176.5, 186.0, 0.6096, 4.572,0]
	calibData4 = [426.0, 191.0, 149.5, 184.5, 0.6096, 3.6576,0]

	calibData = [calibData1,calibData2,calibData3,calibData4]
	
	param1 = np.linspace(0.0013,0.00136,31)
	param2 = np.linspace(0.00124,0.00129,31)
	
	costMap = np.zeros([len(param1),len(param2)])
	
	for i in range(0,len(param1)):
		print(i)
		for j in range(0,len(param2)):
			
			params = [param1[i],param2[j]]
			
			costMap[i,j] = cost_function(params,calibData)

	plt.pcolor(param2,param1,np.log(costMap))
	
	return costMap

cost = calibration()

