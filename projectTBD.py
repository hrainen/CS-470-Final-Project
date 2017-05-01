import tkinter
import time
import sys
import random
from tkinter import *

class ProjectTBD:
	def __init__(self, GUI, time, color):
		self.GUI = GUI
		self.color = color
		self.time = time
		self.chosenPiece = [(0,0),[]]
		self.chosenMove = (0,0)
		
	def calculateMove(self):
		start = time.time()
		while(True):
			if(time.time() - start > self.time):
				self.makeMove()
				return
			if self.color == "green":
				possibleMoves = self.GUI.genMovesGreen()
			else:
				possibleMoves = self.GUI.genMovesRed()
			
			self.chosenPiece = random.choice(list(possibleMoves.items()))
			self.chosenMove = random.choice(list(self.chosenPiece[1]))
		
	def makeMove(self):
		print("Time's up!")
		self.GUI.selectedPiece = self.GUI.board[self.GUI.coordToIndice(self.chosenPiece[0])]
		self.GUI.moveSelectedPiece(self.GUI.board[self.GUI.coordToIndice(self.chosenMove)])
		
		self.GUI.refreshBoard()