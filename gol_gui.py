import PySimpleGUI as sg
import math
from game_of_life import GameOfLife
import time

class GOLGui:
	def __init__(self, size : int):
		self.game = GameOfLife(size)
		self.size = size
		self.canvasWidth = 640
		self.canvasHeight = 480
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

	def drawCells(self) -> None:
		cellWidth = self.canvasWidth / self.size
		cellHeight = self.canvasHeight / self.size
		fillColor = 'black'
		for col in range(self.size):
			x = col * cellWidth
			for row in range(self.size):
				y = row * cellHeight

				cellx, celly = self.getCell(col * cellWidth,row * cellHeight)
				cell = self.game.positions[cellx,celly]
				if cell.isAlive: fillColor = 'white'
				else: fillColor = 'black'
				self.graph.DrawPolygon([(x,y),(x,y+cellHeight),(x+cellWidth,y+cellHeight),(x+cellWidth,y)], line_color="white", line_width= 5, fill_color=fillColor)
	
	def getCell(self, x, y) -> tuple :
		cellx = math.floor(x / (self.canvasWidth / self.size))
		celly = gui.size - 1 - math.floor(y / (self.canvasHeight / self.size))
		return (cellx,celly)

if __name__ == "__main__":

	gui = GOLGui(20)
	gui.game.setPulsarPattern()
	gui.drawCells()

	while True:
		event, values = gui.window.Read()
		if event in (sg.WIN_CLOSED, 'Exit'):
			break
		
		gui.game.step()
		gui.drawCells()

	#	mouse = values['graph']
	#	if event == 'graph':
	#		if mouse == (None, None):
	#			continue
	#		
	#		
	#		
	#		