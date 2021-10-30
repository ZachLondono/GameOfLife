import time
import random
import sys

# ----- Conway's Game Of Life Rules ----- 
# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

class GameOfLife:
	def __init__(self, size : int):
		self.size = size
		self.positions = {} 
		for x in range(size):
			for y in range(size):
				cell = Cell(x,y)
				self.positions[(x,y)] = cell

	def play(self, duration : float):
		self.clear()
		self.draw()
		time.sleep(duration)
		while not self.isExtinct():
			self.clear()
			self.draw()
			self.clear()
			self.step()
			time.sleep(duration)


	def isExtinct(self) -> bool :
		for value in self.positions.values():
			if value.isAlive: return False
		return True

	def randomizeCells(self, chance : float):
		for key in self.positions:
			if random.randint(1, 100) > (1 - chance) * 100:
				self.positions[key].setAlive(True)
			else: self.positions[key].setAlive(False)

	def setBeePattern(self):
		for key in self.positions:
			if key == (1,0) or key == (0,1) or key == (0,2) or key == (2,1) or key == (2,2) or key == (1,3):
				self.positions[key].isAlive = True
			else: self.positions[key].isAlive = False

	def setBlinkerPattern(self):
		for key in self.positions:
			if key == (1,0) or key == (1,1) or key == (1,2):
				self.positions[key].isAlive = True
			else: self.positions[key].isAlive = False

	def setPulsarPattern(self):
		for key in self.positions:
			if key == (4,2) or key == (5,2) or key == (6,2) \
				or key == (2,4) or key == (2,5) or key == (2,6) \
				or key == (4,7) or key == (5,7) or key == (6,7) \
				or key == (7,4) or key == (7,5) or key == (7,6) \
				or key == (4,9) or key == (5,9) or key == (6,9) \
				or key == (9,4) or key == (9,5) or key == (9,6) \
				or key == (10,2) or key == (11,2) or key == (12,2) \
				or key == (2,10) or key == (2,11) or key == (2,12) \
				or key == (7,10) or key == (7,11) or key == (7,12) \
				or key == (9,10) or key == (9,11) or key == (9,12) \
				or key == (14,10) or key == (14,11) or key == (14,12) \
				or key == (14,4) or key == (14,5) or key == (14,6) \
				or key == (4,14) or key == (5,14) or key == (6,14) \
				or key == (10,14) or key == (11,14) or key == (12,14) \
				or key == (10,9) or key == (11,9) or key == (12,9) \
				or key == (10,7) or key == (11,7) or key == (12,7) \
				:
				self.positions[key].isAlive = True
			else: self.positions[key].isAlive = False
	
	def setGliderPattern(self):
		for key in self.positions:
			if key == (1,0) or key == (2,1) or key == (2,2) or key == (1,2) or key == (0,2):
				self.positions[key].isAlive = True
			else: self.positions[key].isAlive = False

	def draw(self):
		string = ""
		for x in range(self.size):
			for y in range(self.size):
				cell = self.positions[(x, y)]
				string += cell.toString()
			string += '\n'
		print(string, end="")

	def step(self):
		nextStep = {}
		for key in self.positions:
			cell = self.positions[key]
			newCell = Cell(key[0], key[1])
			livingNeighbors = 0

			if key[1] > 0 and self.positions[(key[0], key[1] - 1)].isAlive: livingNeighbors += 1
			if key[1] < size-1 and self.positions[(key[0], key[1] + 1)].isAlive: livingNeighbors += 1
			if key[0] > 0 and self.positions[(key[0] - 1, key[1])].isAlive: livingNeighbors += 1
			if key[0] < size-1 and self.positions[(key[0] + 1, key[1])].isAlive: livingNeighbors += 1
			if key[0] > 0 and key[1] > 0 and self.positions[(key[0] - 1, key[1] - 1)].isAlive: livingNeighbors += 1
			if key[0] < size-1 and key[1] < size-1 and self.positions[(key[0] + 1, key[1] + 1)].isAlive: livingNeighbors += 1
			if key[0] > 0 and key[1] < size-1 and self.positions[(key[0] - 1, key[1] + 1)].isAlive: livingNeighbors += 1
			if key[0] < size-1 and key[1] > 0 and self.positions[(key[0] + 1, key[1] - 1)].isAlive: livingNeighbors += 1

			if cell.isAlive and (livingNeighbors == 2 or livingNeighbors == 3):
				newCell.isAlive = True
			elif not cell.isAlive and livingNeighbors == 3:
				newCell.isAlive = True
			else: newCell.isAlive = False

			nextStep[key] = newCell
		self.positions = nextStep

	def clear(self):
		print (u"{}[2J{}[;H".format(chr(27), chr(27)), end="")

class Cell:
	def __init__(self, x : int, y : int):
		self.isAlive = False 
		self.X = x
		self.Y = y
	def setAlive(self, isAlive : bool):
		self.isAlive = isAlive
	def toString(self):
		if self.isAlive: 
			return "[X]"
		else: return "[ ]"

def errPrint():
	print(
f"""Usage: python3 {sys.argv[0]} [OPTIONS]\n\
Try 'python3 {sys.argv[0]} --help' for more information.""")
	exit()

def trySizeFromArgs(param1 : str, param2 : str) -> int:
	if (param1.__eq__("-s") or param1.__eq__("--size")) and param2.isnumeric():
		try:
			return int(param2)
		except ValueError:
			print("Integer value requred for size.")
			exit()
	else: errPrint()

if __name__ == '__main__':
	argCount = len(sys.argv)
	size = 0
	game = None

	if argCount == 1:
		errPrint()
	elif argCount == 2:
		param = sys.argv[1]
		if param.__eq__("--help"):
			print(
f"""Usage: python3 {sys.argv[0]} {{-s|--size}} <SIZE> [PATTERN]
Play Conway's Game of Life.
Example: 'python3 {sys.argv[0]} -r -s 10'

	-s, --size <SIZE>		set the size of the board

Pattern Options:
	-r, --rand			populate the board with random cells
	--bee				stable beehive pattern
	--blinker			oscillating blinker
	--pulsar			oscillating pulsar
	--glider			glider spaceship""")
			exit()
		else: errPrint()
	elif argCount == 3:
		param1 = sys.argv[1]
		param2 = sys.argv[2]
		size = trySizeFromArgs(param1, param2)
		game = GameOfLife(size)
		game.randomizeCells(0.2)
	elif argCount == 4:
		param1 = sys.argv[1]
		param2 = sys.argv[2]
		size = trySizeFromArgs(param1, param2)
		game = GameOfLife(size)
		param3 = sys.argv[3]
		if param3.__eq__("-r") or param3.__eq__("--rand"):
			game.randomizeCells(0.2)
		elif param3.__eq__("--bee"):
			game.setBeePattern()
		elif param3.__eq__("--blinker"):
			game.setBlinkerPattern()
		elif param3.__eq__("--pulsar"):
			game.setPulsarPattern()
		elif param3.__eq__("--glider"):
			game.setGliderPattern()
		else: errPrint()

	game.play(0.25)