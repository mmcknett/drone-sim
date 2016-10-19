from model2d import *
from env2d import *
import math

class ConstantThrustController:
	def __init__(self, drone, env):
		self.drone = drone
	
	def setThrust(self, currentTime):
		self.drone.setThrustL(5)
		self.drone.setThrustR(5)

class VariableController:
	def __init__(self, drone, env):
		self.drone = drone
	
	def setThrust(self, currentTime):
		if currentTime < 1.5 and currentTime > 1.4:
			tl = 5.1
			tr = 5
		elif currentTime > 1.5 and currentTime < 3.0:
			tl = 5.05
			tr = 5.05
		elif currentTime > 3.0 and currentTime < 3.1:
			tl = 4.91
			tr = 5.12
		elif currentTime > 3.1 and currentTime < 4.0:
			tl = 5.05
			tr = 5.05
		elif currentTime > 4.0 and currentTime < 4.1:
			tl = 5.1
			tr = 5
		else:
			tl = 5
			tr = 5

		self.drone.setThrustL(tl)
		self.drone.setThrustR(tr)
