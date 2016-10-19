import math
import numpy as np
import unittest
import pdb

class DronePos:
	""" Describes the position and rotation of the drone. """
	def __init__(self, x, y, t):
		self.x = x
		self.y = y
		self.t = t

	def __str__(self):
		return "({0}, {1}, {2})".format(self.x, self.y, self.t)

	def __repr__(self):
		return self.__str__()

class DroneVel:
	""" Describes the velocity and angular velocity of the drone. """
	def __init__(self, vx, vy, w):
		self.vx = vx
		self.vy = vy
		self.w = w

class Drone2d:
	""" The model of a 2d bicopter """
	cMaxThrust = 20
	cRadius = 0.5

	def __init__(self):
		""" By default, the drone is 1kg, positioned at 0,0 with no
		rotation, and traveling at 0 velocity and angular velocity. """
		self.initialize(DronePos(0, 0, 0), DroneVel(0, 0, 0), 1)
		self.thrustL = 0
		self.thrustR = 0

	def initialize(self, initialPos, initialVel, mass):
		self.pos = initialPos
		self.vel = initialVel
		self.mass = mass

	def setThrustL(self, thrust):
		thrust = max(thrust, 0)
		self.thrustL = min(thrust, self.cMaxThrust)

	def setThrustR(self, thrust):
		thrust = max(thrust, 0)
		self.thrustR = min(thrust, self.cMaxThrust)

	def getThrust(self):
		totalThrust = self.thrustL + self.thrustR
		# Thrust is along the Y axis when the angle is 0.
		thrustX = totalThrust * math.sin(self.pos.t)
		thrustY = totalThrust * math.cos(self.pos.t)
		return [thrustX, thrustY]

	def getAngularAccel(self):
		""" Angular acceleration due to thrust, assuming that the
		drone has uniform mass and is a rod of length 2 * cRadius """
		thrustDiff = self.thrustL - self.thrustR
		return (3 * thrustDiff) / (self.mass * self.cRadius)


class DroneUnitTests(unittest.TestCase):

	def test_setThrustL_LessThan0_ThrustLIs0(self):
		# Arrange
		drone = Drone2d()
		
		# Act	
		drone.setThrustL(-5)

		# Assert
		self.assertEqual(drone.thrustL, 0)
		

	def test_setThrustL_LessThanMaxThrust_ThrustAsSet(self):
		# Arrange
		drone = Drone2d()

		# Act
		drone.setThrustL(5)

		# Assert
		self.assertEqual(drone.thrustL, 5)

	def test_setThrustL_GreaterThanMaxThrust_ThrustLIsMaxThrust(self):
		# Arrange
		drone = Drone2d()

		# Act
		drone.setThrustL(drone.cMaxThrust + 5)

		# Assert
		self.assertEqual(drone.thrustL, drone.cMaxThrust)

	def test_setThrustR_LessThan0_ThrustRIs0(self):
		# Arrange
		drone = Drone2d()

		# Act
		drone.setThrustR(-5)

		# Assert
		self.assertEqual(drone.thrustR, 0)
	
	def test_setThrustR_LessThanMaxThrust_ThrustAsSet(self):
		# Arrange
		drone = Drone2d()

		# Act
		drone.setThrustR(5)

		# Assert
		self.assertEqual(drone.thrustR, 5)

	def test_setThrustR_GreaterThanMaxThrust_ThrustRIsMaxThrust(self):
		# Arrange
		drone = Drone2d()

		# Act
		drone.setThrustR(drone.cMaxThrust + 5)

		# Assert
		self.assertEqual(drone.thrustR, drone.cMaxThrust)

	def test_getThrustVector_LAndRThrust_ThrustYIsSumOfLAndR(self):
		# Arrange
		drone = Drone2d()
		drone.setThrustL(2)
		drone.setThrustR(2)

		# Act
		thrustVector = drone.getThrust()

		# Assert
		self.assertAlmostEqual(thrustVector[0], 0)
		self.assertAlmostEqual(thrustVector[1], 4)

	def test_getThrustVector_LAndRThrust90DegreeBank_ThrustXIsSumOfLAndR(self):
		# Arrange
		drone = Drone2d()
		drone.initialize(DronePos(0, 0, math.pi / 2), DroneVel(0, 0, 0), 1)

		drone.setThrustL(2)
		drone.setThrustR(2)

		# Act
		thrust = drone.getThrust()

		# Assert
		self.assertAlmostEqual(thrust[0], 4)
		self.assertAlmostEqual(thrust[1], 0)

if __name__ == '__main__':
	unittest.main()

