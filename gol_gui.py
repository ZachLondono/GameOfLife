import PySimpleGUI as sg
import math
from game_of_life import GameOfLife
import time
import threading

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
					),
					sg.Button(
						key="pause_btn",
						button_text="pause"
					),
					sg.Button(
						key="step_btn",
						button_text="setp"
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
		self.cells.clear()

		# Redraw all living cells
		for col in range(self.size):
			x = col * cellWidth
			for row in range(self.size):
				y = row * cellHeight
				cellx, celly = self.getCell(col * cellWidth,row * cellHeight)
				cell = self.game.positions[cellx,celly]
				if cell.isAlive: 
					poly = self.graph.DrawPolygon([(x,y),(x,y+cellHeight),(x+cellWidth,y+cellHeight),(x+cellWidth,y)],fill_color='white')
					self.cells.append(poly)
	
	def getCell(self, x, y) -> tuple :
		cellx = math.floor(x / (self.canvasWidth / self.size))
		celly = gui.size - 1 - math.floor(y / (self.canvasHeight / self.size))
		return (cellx,celly)

def run(gui, pause_event):
	while True:
		time.sleep(0.25)
		global pause_updater
		if pause_updater:
			pause_event.wait()
			pause_event.clear()
		gui.game.step()
		global stop_updater
		if stop_updater: break
		gui.window.write_event_value("update", "val")

if __name__ == "__main__":

	gui = GOLGui(50)
	#gui.game.setPulsarPattern()
	gui.game.randomizeCells(0.2)
	#gui.game.setBlinkerPattern()
	#gui.game.setGliderPattern()
	gui.drawCells()

	stop_updater = False 
	pause_updater = False
	pause_event = threading.Event()
	updateThread = threading.Thread(target=run, args=(gui,pause_event))
	updateThread.start()

	while True:
		event, values = gui.window.read()
		if event is None:
			pause_updater = False
			stop_updater = True
			pause_event.set()
			updateThread.join()
			break

		if event == "update":
			gui.drawCells()
			gui.window.refresh()
		elif event == 'pause_btn':
			if pause_updater == True:
				pause_updater = False
				pause_event.set()
			else: 
				pause_event.clear()
				pause_updater = True
		elif pause_updater == True:
			if  event == 'graph':
				mouse = values['graph']
				x = mouse[0]
				y = mouse[1]
				cellPos = gui.getCell(x,y)
				gui.game.positions[cellPos].isAlive = not gui.game.positions[cellPos].isAlive
				gui.drawCells()
				gui.window.refresh()
			elif event == 'step_btn':
				gui.game.step()
				gui.drawCells()
				gui.window.refresh()