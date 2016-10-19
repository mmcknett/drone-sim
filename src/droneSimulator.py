import env2d
import model2d
import math


def applyAccel(posPrev, velPrev, accel, timeStep):
	vel = velPrev + accel * timeStep
	pos = posPrev + velPrev * timeStep + 0.5 * accel * timeStep**2
	return (pos, vel)

def applyForce(force, drone, timeStep):
	forceX = force[0]
	forceY = force[1]
	(newX, newVx) = applyAccel(drone.pos.x, drone.vel.vx, forceX / drone.mass, timeStep)
	(newY, newVy) = applyAccel(drone.pos.y, drone.vel.vy, forceY / drone.mass, timeStep)

	alpha = drone.getAngularAccel()
	(newT, newW) = applyAccel(drone.pos.t, drone.vel.w, alpha, timeStep)
	drone.pos = DronePos(newX, newY, newT)
	drone.vel = DroneVel(newVx, newVy, newW)

def doOneStep(env, drone, timeStep):
	# The forces on the drone, currently, are gravity, the drone's thrust,
	# and the resistance from the wind.
	thrust = drone.getThrust()
	forceX = env.gravityX() + thrust[0]
	forceY = env.gravityY() + thrust[1]
	applyForce([forceX, forceY], drone, timeStep)

def runSimulation(env, drone, controller, timeStep, totalTime):
	""" Provide the environment and drone for the simulation,
	along with the time step between each calculation point and
	the total time to run the simulation (unless the drone crashes) """
	
	currentTime = 0
	positionTrace = [(drone.pos, currentTime)]
	while currentTime < totalTime and drone.pos.y > 0:
		controller.setThrust(currentTime)
		doOneStep(env, drone, timeStep)
		currentTime += timeStep
		positionTrace.append((drone.pos, currentTime))

	return positionTrace

from model2d import *
from env2d import *
from droneControl import *
import matplotlib.pyplot as plt

def plotResult(result):
	# Plot the resulting angle and position.
	time = [entry[1] for entry in result]
	angles = [entry[0].t for entry in result]
	heights = [entry[0].y for entry in result]
	xs = [entry[0].x for entry in result]

	plt.subplot(211)
	plt.title("Rotation over time")
	plt.plot(time, angles)

	plt.subplot(212)
	plt.title("Position over time")
	plt.plot(time, heights)
	plt.plot(time, xs)
	plt.show()

def defaultSimulation():
	drone = Drone2d()
	drone.initialize(DronePos(0, 2, 0), DroneVel(0, 0, 0), 1)
	env = Environment2d()

	#controller = ConstantThrustController(drone, env)
	controller = VariableController(drone, env)
	
	print("Starting the drone at {0}".format(drone.pos))
	
	result = runSimulation(env, drone, controller, 0.1, 10)
	plotResult(result)

	return result

if __name__ == "__main__":
	defaultSimulation()
