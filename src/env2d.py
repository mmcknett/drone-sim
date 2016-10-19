class Environment2d:
	def __init__(self):
		self.windSpeed = 0
		self._gravity = [0, -10]

	def gravityX(self):
		return self._gravity[0]

	def gravityY(self):
		return self._gravity[1]
