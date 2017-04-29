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
		self.GUI.selectedPiece = self.GUI.board[(chosenPiece[0])[0] + self.GUI.dim*(chosenPiece[0])[1]]
		chosenMove = random.choice(list(chosenPiece[1]))
		self.GUI.moveSelectedPiece(self.GUI.board[chosenMove[0] + self.GUI.dim*chosenMove[1]])
		
		self.GUI.refreshBoard()