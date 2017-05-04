import tkinter
import time
import sys
import random
from tkinter import *

class ProjectTBD:
	def __init__(self, GUI, time, color):
		self.GUI = GUI
		self.color = color
		if self.color == "green":
			self.enemyColor = "red"
		else:
			self.enemyColor = "green"
		self.time = time
		self.chosenPiece = [(0,0),[]]
		self.chosenMove = (0,0)
		
	def calculateMove(self):
		start = time.time()
		numPly = 1
		
		board = self.GUI.genSimpleBoard()
		print(self.heuristicOfBoard(board))
		possibleMoves = self.genMoves(board, self.color)
		
		self.chosenPiece = random.choice(list(possibleMoves.items()))
		self.chosenMove = random.choice(list(self.chosenPiece[1]))
			
		while(True):
			if time.time() - start > self.time/2:
				self.makeMove()
				break
			#chosenPair = self.minimax(possibleMoves, board, numPly)
			#self.chosenPiece = chosenPair[0]
			#self.chosenMove = chosenPair[1]
			numPly += 1
		
	def makeMove(self):
		print("Time's up!")
		self.GUI.selectedPiece = self.GUI.board[self.GUI.coordToIndice(self.chosenPiece[0])]
		self.GUI.moveSelectedPiece(self.GUI.board[self.GUI.coordToIndice(self.chosenMove)])
		
		self.GUI.refreshBoard()
		
	def minimax(self, possibleMoves, board, numPly):
		pass
	
	def heuristicOfBoard(self, board):
		redCorner = self.GUI.dim-1					#this is the farthest corner in the red base
		redCornerCoord = self.GUI.indiceToCoord(redCorner)
		grnCorner = (self.GUI.dim*(self.GUI.dim-1))	#this is the farthest corner in the grn base
		grnCornerCoord = self.GUI.indiceToCoord(grnCorner)
		totalStraightLineDistance = 0
		
		for i in range(self.GUI.dim):	#Find distance of each computer piece from opposite corner
			for j in range(self.GUI.dim):
				if board[self.GUI.coordToIndice((i, j))] == 'O' and self.color == "green":
					totalStraightLineDistance += self.heuristicVal((i,j), redCornerCoord)
				elif board[self.GUI.coordToIndice((i, j))] == 'X' and self.color == "red":
					totalStraightLineDistance += self.heuristicVal((i,j), grnCornerCoord)
		return -totalStraightLineDistance
		
	def heuristicVal(self, pos, newPos):
		redCorner = self.GUI.dim-1					#this is the farthest corner in the red base
		redCornerCoord = self.GUI.indiceToCoord(redCorner)
		grnCorner = (self.GUI.dim*(self.GUI.dim-1))	#this is the farthest corner in the grn base
		grnCornerCoord = self.GUI.indiceToCoord(grnCorner)

		if self.color == "green":
			posDist = int(((redCornerCoord[1]-pos[1])**2+(redCornerCoord[0]-pos[0])**2)**(1/2))
			newPosDist = int(((redCornerCoord[1]-newPos[1])**2+(redCornerCoord[0]-newPos[0])**2)**(1/2))
		else:
			#distance between two points = sqrt((Ynew - Yold)^2+(Xnew-Xold)^2)
			posDist = int(((grnCornerCoord[1]-pos[1])**2+(grnCornerCoord[0]-pos[0])**2)**(1/2))
			# then find distance between the potential spot we want to move to, and the green corner
			newPosDist = int(((grnCornerCoord[1]-newPos[1])**2+(grnCornerCoord[0]-newPos[0])**2)**(1/2))
			
		# this is a positive or negative value depending on if were moving towards the enemy corner or away from it
		delta = posDist - newPosDist # just compares distance from original spot to enemy base, and dist from new spot to enemy base
		# some helper print statements to see what is going on.
		print(pos, "to", newPos, " distance: ", delta)
		return delta
	
	def makeTempMove(self, start, end, board):
		pieceToMove = board[start]
		board[start] = ' '
		board[end] = pieceToMove
		return board
	
	def genMoves(self, board, color):
		self.allValMoves = {} 		# append dictionaries for pieces and their valid moves here

		# loop through the board, if the piece being checked belongs to the player whos moves we're generating
		if color == "green":
			for i in range(self.GUI.dim*self.GUI.dim):
				if board[i] == "O": # generate valid moves for that piece
					self.allValMoves.update(self.getValidMoves(i, board))
		else:
			for i in range(self.GUI.dim*self.GUI.dim):
				if board[i] == "X": # generate valid moves for that piece
					self.allValMoves.update(self.getValidMoves(i, board))
		return self.allValMoves
		
	def getValidMoves(self, pos, board):
		self.X = pos % self.GUI.dim 			# converts indice to X-coord
		self.Y = pos // self.GUI.dim			# converts indice to Y-coord
		self.coord = (self.X, self.Y)		# 2-tuple for the coord (X,Y)
		self.valMoves = []					# List to store all valid coordinates(X,Y) at

		# the coordinates of adjacent squares
		self.adjPos = [(-1,-1),(0,-1),(1,-1),
					   (-1,0),        (1,0),
					   (-1,1), (0,1), (1,1)]

		# check to see if all adjacent moves are valid
		for j in self.adjPos:
			self.newX = self.X + j[0] # gets the actual adjacent X value
			self.newY = self.Y + j[1] # gets the actual adjacent Y value
			self.newCoord = (self.newX, self.newY)

			self.newIndice = self.newCoord[0] + self.newCoord[1]*self.GUI.dim


			# checks if the adjacent X position is in bounds
			if self.newX >= 0 and self.newX < self.GUI.dim:
				# checks if the adjacent Y position is in bounds
				if self.newY >= 0 and self.newY < self.GUI.dim:
					#  if the position is blank (no piece is there)
					if board[self.newIndice] == " ":
						# add that position to the list of valid positions
						self.valMoves.append(self.newCoord)

		# check if there are any jumps for the initial piece passed in
		self.jumps = list(self.getJumps(self.coord, [], board))
		if self.jumps != None:
			self.valMoves = self.valMoves + list(self.jumps)
		#print("jumps: ", self.coord, ":", self.jumps)
		
		validatedMoves = []		#Filters moves based on whether they follow territory rules
		for move in self.valMoves:
			if self.territoryConflict(self.GUI.coordToIndice(self.coord), self.GUI.coordToIndice(move), board):
				continue
			validatedMoves.append(move)
		return {self.coord: validatedMoves} 	#returns valid positions for one piece to move to

	# @ params: takes in the position you want to jump to, and the list of seen positions
	# returns a list of valid positions something can jump to.
	def getJumps(self, pos, seen, board):
		self.valJumps = [] # keeps track of valid jump positions.
		self.newSeen = list(seen)  # new seen list to add any valid jumps we visit to

		#coords of potential adjacent jumps
		self.adjJumps = [(-2, -2), (0, -2), (2, -2),
						 (-2, 0), 			(2, 0),
						 (-2, 2), (0, 2),   (2, 2)]

		# the coordinates of potential adjacent pieces to jump over
		self.adjPos = [(-1, -1), (0, -1), (1, -1),
					   (-1, 0), 		  (1, 0),
					   (-1, 1),  (0, 1),  (1, 1)]

		for z in range(0,8):
			self.newAdjX = pos[0] + self.adjPos[z][0]
			self.newAdjY = pos[1] + self.adjPos[z][1]
			self.newAdjCoord = (self.newAdjX, self.newAdjY)

			self.adjIndic = self.newAdjCoord[0] + self.newAdjCoord[1]*self.GUI.dim


			self.jumpX = pos[0] + self.adjJumps[z][0]  # gets the jump X value
			self.jumpY = pos[1] + self.adjJumps[z][1]  # gets the jump Y value
			self.jumpCoord = (self.jumpX, self.jumpY) # makes tuple for the X,Y for the jump coord

			# convert new jump (X,Y) to an indice
			self.jIndice = self.jumpCoord[0] + self.jumpCoord[1] * self.GUI.dim


			# check if jumpcoord is in bounds
			if self.jumpX >= 0 and self.jumpX < self.GUI.dim:
				if self.jumpY >= 0 and self.jumpY < self.GUI.dim:
					# and not in list of seen positions.
					if self.jumpCoord not in seen:
						# if there is a piece before the jump
						if board[self.adjIndic] != " ":
							# and the spot we want to jump to is not occupied by a piece, add to valid moves
							if board[self.jIndice] == " ":
								self.valJumps.append(self.jumpCoord)
								self.newSeen.append(self.jumpCoord)

		# recursively find any more jump positions, update seen to have the place we just jumped to
		for valJump in self.valJumps:
			self.valJumps = self.valJumps + list(self.getJumps(valJump, self.newSeen, board))

		if self.valJumps != None:
			return self.valJumps
		else:
			return None
			
	def territoryConflict(self, start, end, board):	#Checks to see if a player is trying an illegal move concerning territories
		#If green is in enemy territory, it cannot move back out
		if board[start] == 'O' and self.GUI.inTopRight(start//self.GUI.dim, start%self.GUI.dim):
			if not self.GUI.inTopRight(end//self.GUI.dim, end%self.GUI.dim):
				return True
		#If green is outside of its home territory, it may not move back
		elif board[start] == 'O' and not self.GUI.inBottomLeft(start//self.GUI.dim, start%self.GUI.dim):
			if self.GUI.inBottomLeft(end//self.GUI.dim, end%self.GUI.dim):
				return True
		#Same rules as above, except for red
		if board[start] == 'X' and self.GUI.inBottomLeft(start//self.GUI.dim, start%self.GUI.dim):
			if not self.GUI.inBottomLeft(end//self.GUI.dim, end%self.GUI.dim):
				return True
		elif board[start] == 'X' and not self.GUI.inTopRight(start//self.GUI.dim, start%self.GUI.dim):
			if self.GUI.inTopRight(end//self.GUI.dim, end%self.GUI.dim):
				return True