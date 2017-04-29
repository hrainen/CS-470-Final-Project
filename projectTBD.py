import tkinter
import time
import sys
import random
from tkinter import *

class ProjectTBD:
	def __init__(self, GUI, color):
		self.GUI = GUI
		self.color = color
		
	def makeMove(self):
		if self.color == "green":
			possibleMoves = self.GUI.genMovesGreen()
		else:
			possibleMoves = self.GUI.genMovesRed()
		
		chosenPiece = random.choice(list(possibleMoves.items()))
		self.GUI.selectedPiece = self.GUI.board[self.GUI.coordToIndice(chosenPiece[0])]
		chosenMove = random.choice(list(chosenPiece[1]))
		self.GUI.moveSelectedPiece(self.GUI.board[self.GUI.coordToIndice(chosenMove)])
		
		self.GUI.refreshBoard()