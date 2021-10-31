import PySimpleGUI as sg
import math
from game_of_life import GameOfLife
import time
import threading
import ctypes

class GOLGui:
	def __init__(self, size : int):
		self.game = GameOfLife(size)
		self.size = size
		self.canvasWidth = 700
		self.canvasHeight = 700
		self.layout = [
				[
					sg.Graph(
						canvas_size=(self.canvasWidth, self.canvasHeight),
						graph_bottom_left=(0, 0),
						graph_top_right=(self.canvasWidth,self.canvasHeight),
						key="graph",
						background_color='black',
						enable_events=True
					)
				]
			]
		self.window = sg.Window("Game of Life", self.layout, background_color= 'black')
		self.window.Finalize()
		self.graph = self.window.Element("graph")
		self.cells = []

	def drawCells(self) -> None:
		cellWidth = self.canvasWidth / self.size
		cellHeight = self.canvasHeight / self.size
		
		# Clear the graph
		for cell in self.cells:
			self.graph.delete_figure(cell)
		
		# Reset list of living cells
		self.cells = []

		# Redraw all living cells
		for col in range(self.size):
			x = col * cellWidth
			for row in range(self.size):
				y = row * cellHeight
				cellx, celly = self.getCell(col * cellWidth,row * cellHeight)
				cell = self.game.positions[cellx,celly]
				if cell.isAlive: 
					poly = self.graph.DrawPolygon([(x,y),(x,y+cellHeight),(x+cellWidth,y+cellHeight),(x+cellWidth,y)], fill_color='white')
					self.cells.append(poly)
	
	def getCell(self, x, y) -> tuple :
		cellx = math.floor(x / (self.canvasWidth / self.size))
		celly = gui.size - 1 - math.floor(y / (self.canvasHeight / self.size))
		return (cellx,celly)

def run(gui):
	while True:
		time.sleep(0.25)
		gui.game.step()
		global stop_updater
		if stop_updater: break
		print("Sending update")
		gui.window.write_event_value("update", "val")
		print("update sent")
	print("Done updater thread")

if __name__ == "__main__":

	gui = GOLGui(50)
	gui.game.setPulsarPattern()
	#gui.game.randomizeCells(0.2)
	#gui.game.setBlinkerPattern()
	#gui.game.setGliderPattern()
	gui.drawCells()

	stop_updater = False 
	updateThread = threading.Thread(target=run, args=(gui,))
	updateThread.start()

	while True:
		event, values = gui.window.read()
		if event is None:
			break
		if event == "update":
			gui.drawCells()
			gui.window.refresh()
	
	stop_updater = True
	updateThread.join()
	print("Done main thread")
