from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import time

t_length = 30

t = np.linspace(0,t_length,301)

x = np.cos(t*2)

y = np.sin(t*3)

z = 0.1*t

fig = plt.figure()
ax = fig.gca(projection='3d')

for i in range(10, len(t)):
	
	time.sleep(0.01)
	ax.clear()
	ax.plot(x[i-10:i+1],y[i-10:i+1],z[i-10:i+1])

	ax.scatter(x[i],y[i],z[i])
	ax.set_xlim([-2,2])
	ax.set_ylim([-2,2])
	ax.set_zlim([-2,2])
	fig.canvas.draw()
	fig.canvas.flush_events()