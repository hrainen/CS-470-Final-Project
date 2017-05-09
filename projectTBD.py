import tkinter
import time
import sys
import random
from tkinter import *

class ProjectTBD:
	def __init__(self, GUI, time, color):
		self.GUI = GUI
		self.color = color
		self.plyLimit = 0
		self.start = 0
		self.nodesQueued = 0
		self.nodesExplored = 0
		self.boardStatesEvaluated = 0
		self.numPruningEvents = [0]
		self.doAlphaBeta = True
		
		#coords of potential adjacent jumps
		self.adjJumps = [(-2, -2), (0, -2), (2, -2),
						 (-2, 0), 			(2, 0),
						 (-2, 2), (0, 2),   (2, 2)]

		# the coordinates of potential adjacent pieces
		self.adjPos = [(-1,-1),(0,-1),(1,-1),
					   (-1,0),        (1,0),
					   (-1,1), (0,1), (1,1)]
		
		if self.color == "green":
			self.enemyColor = "red"
		else:
			self.enemyColor = "green"
		self.time = time
		self.chosenPiece = [(0,0),[]]
		self.chosenMove = (0,0)
	
	def resetData(self, numPly):
		self.nodesQueued = 0
		self.nodesExplored = 0
		self.boardStatesEvaluated = 0
		self.numPruningEvents = []
		for i in range(numPly):
			self.numPruningEvents.append(0)
	
	def calculateMove(self):	#This function activates minimax in the first place
		self.start = time.time()
		numPly = 1
		self.resetData(numPly)
		
		board = self.GUI.genSimpleBoard()
		#print(self.heuristicOfBoard(board))
		possibleMoves = self.genMoves(board, self.color)	#Select a random starting move, in case something goes wrong with minimax
		if possibleMoves != []:
			self.chosenPair = random.choice(list(possibleMoves.items()))
			if self.chosenPair != [] and self.chosenPair[1] != []:
				self.chosenPiece = self.chosenPair[0]
				self.chosenMove = random.choice(list(self.chosenPair[1]))
			
		while(True):
			if time.time() - self.start > self.time - 1:	#Once time has run out, make the selected move
				print("Time's up!")
				print("Stopped at %f seconds" % (time.time() - self.start))
				print("\n~~~~~~~~~~~~~~~~~~~~~~\n")
				self.makeMove()
				break
			board = self.GUI.genSimpleBoard()
			chosenPair = self.minimax(board, numPly)
			if chosenPair != None:	#If minimax returns something, change the current selected move
				self.chosenPiece = chosenPair[0]
				self.chosenMove = chosenPair[1]
				print("Ply %d reached" % numPly)
				print("%d explored nodes" % self.nodesExplored)
				print("%d alpha beta pruning events, at ply [0 1 ...] -> [%s]" % (sum(self.numPruningEvents), ' '.join(str(x) for x in self.numPruningEvents)))
				print("%d nodes pruned (%.1f%%)" % (self.nodesQueued - self.nodesExplored, 100 - 100.0*self.nodesExplored/self.nodesQueued))
				print("%d calculated board states" % self.boardStatesEvaluated)
				print("Time taken: %.4f seconds\n" % (time.time() - self.start))
				numPly += 1
			self.resetData(numPly)
		
	def makeMove(self):	#Makes the final move decided by the computer
		#print(self.chosenPiece[0])
		#print("%d, %d" % (self.chosenMove[0], self.chosenMove[1]))
		self.GUI.selectedPiece = self.GUI.board[self.GUI.coordToIndice(self.chosenPiece)]
		self.GUI.moveSelectedPiece(self.GUI.board[self.GUI.coordToIndice(self.chosenMove)])
		
		self.GUI.refreshBoard()
		
		
	def minimax(self, board, numPly):	#This gets the whole max/min tree running
		alpha = -10000000				#Starting alpha beta values
		beta = 10000000

		self.plyLimit = numPly			#Set ply limit for maximum to use
		heuristicScore = self.heuristicOfBoard(board)
		self.nodesQueued += 1
		self.boardStatesEvaluated += 1
		result = self.alphaBeta(board, 0, alpha, beta, True, heuristicScore)	#Give maximum the current board, set current ply to 0
		
		if result == None or result[0] == 10000000 or result[0] <= -999 or result[0] == None or result[1] == None:
			return None
		return [result[1], result[2]]	#Return movement results
		
	def getNumberOfNodesQueued(self, possibleMoves):
		for piece,moves in possibleMoves.items():
			self.nodesQueued += len(moves)
	
	def returnMax(self, depth, bestMove):
		if depth == 0:
			return bestMove
		return bestMove[0]
	
	def alphaBeta(self, board, depth, alpha, beta, maximizingPlayer, heuristicScore):
		self.nodesExplored += 1
		if depth >= self.plyLimit:	#Base case. If ply limit reached, return current heuristicScore
			self.boardStatesEvaluated += 1
			if self.gameWon(board, self.color):
				return 1000
			return heuristicScore
		
		if time.time() - self.start > self.time - 1:
			if depth == 0 and maximizingPlayer:	#If time has run out, pass the 10000000 flag up the tree
				return [10000000, None, None]
			return 10000000
		
		if maximizingPlayer:
			bestMove = [-999, None, None]	#Holds the best move  ("v = -inf")
			possibleMoves = self.genMoves(board, self.color)	#If not, get all possible friendly moves
			self.getNumberOfNodesQueued(possibleMoves)
			for piece,moves in possibleMoves.items():			#Iterate through these moves, and send new board states to minimax
				for move in moves:
					delta = self.heuristicVal(piece, move)		#FORWARD PRUNING
					if delta < 0:
						continue
					boardCopy = board[:]	#Create copy of board
					boardCopy = self.makeTempMove(self.GUI.coordToIndice(piece), self.GUI.coordToIndice(move), boardCopy)
					
					#Get moves returned from minimum node, store largest heuristic received, tempMove is essentially "v"
					tempMove = [self.alphaBeta(boardCopy, depth, alpha, beta, False, heuristicScore + delta), piece, move]
					if self.gameWon(boardCopy, self.color):
						tempMove[0] = 1000
						return self.returnMax(depth, tempMove)
					
					if tempMove[0] == 10000000:	#If time has run out, this flag (10000000) must be passed to the top
						return self.returnMax(depth, tempMove)
						
					if tempMove[0] > bestMove[0]:	#This is essentially: v := max(v, alphabeta(child...)) on the wiki
						bestMove = tempMove
						
					alpha = max(alpha, tempMove[0])	#If current heuristic is larger than alpha, replace alpha
					if beta <= alpha and self.doAlphaBeta:	#If alpha is ever greater than beta, ignore all other branches, return current best move
						self.numPruningEvents[depth] += 1
						return self.returnMax(depth, bestMove)	#The return BREAKS from loop by quitting function
					
			return self.returnMax(depth, bestMove)
		else:
			worstMove = 0		#Holds the worst move heuristic for computer ("v = inf")

			possibleMoves = self.genMoves(board, self.enemyColor)	#Get all possible enemy moves
			self.getNumberOfNodesQueued(possibleMoves)
			for piece,moves in possibleMoves.items():	#Iterates through all moves, and sends new board states to maximum
				for move in moves:
					delta = self.heuristicVal(piece, move)	#FORWARD PRUNING
					if delta > 0:
						continue
					boardCopy = board[:]	#Copy of board
					boardCopy = self.makeTempMove(self.GUI.coordToIndice(piece), self.GUI.coordToIndice(move), boardCopy)
					if self.gameWon(boardCopy, self.enemyColor):
						return -1000
					#Get moves returned from maxmimum node, store move with smallest heuristic	(or "v")
					tempMove = self.alphaBeta(boardCopy, depth + 1, alpha, beta, True, heuristicScore + delta)
					
					if tempMove == 10000000:	#If time has run out, this flag (10000000) must be passed to the top
						return tempMove
						
					if tempMove < worstMove:	#This is essentially: v := min(v, alphabeta(child...))
						worstMove = tempMove
					
					beta = min(beta, tempMove)	#Get new beta value if a smaller heuristic (than beta) is found
					if beta <= alpha and self.doAlphaBeta:	#If the beta value ever gets lower than alpha, prune all other branches
						self.numPruningEvents[depth] += 1
						return worstMove		#Return current worst heuristic ("v")
												#The return BREAKS from loop by quitting function
			return worstMove				#Return worst heuristic
	
	def heuristicOfBoard(self, board):	#Returns heuristic value of entire board
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
		#delta = 0
		#redCorner = self.GUI.dim-1					#this is the farthest corner in the red base
		#redCornerCoord = self.GUI.indiceToCoord(redCorner)
		#grnCorner = (self.GUI.dim*(self.GUI.dim-1))	#this is the farthest corner in the grn base
		#grnCornerCoord = self.GUI.indiceToCoord(grnCorner)

		if self.color == "green":
			redCornerCoord = self.GUI.indiceToCoord(self.GUI.dim-1)
			#posDist = ((redCornerCoord[1]-pos[1])**2+(redCornerCoord[0]-pos[0])**2)**(1/2)
			#newPosDist = ((redCornerCoord[1]-newPos[1])**2+(redCornerCoord[0]-newPos[0])**2)**(1/2)

			delta =  ((redCornerCoord[1]-pos[1])**2+(redCornerCoord[0]-pos[0])**2)**(1/2) -\
					((redCornerCoord[1]-newPos[1])**2+(redCornerCoord[0]-newPos[0])**2)**(1/2)

                        # if new piece makes into enemy base, add more points
			if not self.GUI.inTopRight(pos[1], pos[0]):
				if self.GUI.inTopRight(newPos[1], newPos[0]):
					delta += 3

			# if new pos is top right diagonal add two points
			if newPos[1] < pos[1] and newPos[0] > pos[0]:
				delta += 2

			# if new pos is up, add one point
			if newPos[1] < pos[1]:
				delta += 1

			#if new pos is right, add one point
			if newPos[0] > pos[0]:
				delta += 1
			
		else:
			grnCornerCoord = self.GUI.indiceToCoord(self.GUI.dim*(self.GUI.dim-1))
			#distance between two points = sqrt((Ynew - Yold)^2+(Xnew-Xold)^2)
			#posDist = ((grnCornerCoord[1]-pos[1])**2+(grnCornerCoord[0]-pos[0])**2)**(1/2)
			# then find distance between the potential spot we want to move to, and the green corner
			#newPosDist = ((grnCornerCoord[1]-newPos[1])**2+(grnCornerCoord[0]-newPos[0])**2)**(1/2)

			delta = ((grnCornerCoord[1]-pos[1])**2+(grnCornerCoord[0]-pos[0])**2)**(1/2) -\
					((grnCornerCoord[1]-newPos[1])**2+(grnCornerCoord[0]-newPos[0])**2)**(1/2)
					

                        # if new piece makes into enemy base, add more points
			if not self.GUI.inBottomLeft(pos[1], pos[0]):
				if self.GUI.inBottomLeft(newPos[1], newPos[0]):
					delta += 3

			# if new pos is top right diagonal add two points
			if newPos[1] > pos[1] and newPos[0] < pos[0]:
				delta += 2

			# if new pos is up, add one point
			if newPos[1] > pos[1]:
				delta += 1

			# if new pos is right, add one point
			if newPos[0] < pos[0]:
				delta += 1
			
		# this is a positive or negative value depending on if were moving towards the enemy corner or away from it
		#delta += posDist - newPosDist # just compares distance from original spot to enemy base, and dist from new spot to enemy base
		# some helper print statements to see what is going on.
		#print(pos, "to", newPos, " distance: ", delta)
		return delta
	
	def makeTempMove(self, start, end, board):	#Alter temporary board state based on move specified by start and end
		board[start], board[end] = board[end], board[start]
		return board
	
	def genMoves(self, board, color):
		self.allValMoves = {} 		# append dictionaries for pieces and their valid moves here

		# loop through the board, if the piece being checked belongs to the player whos moves we're generating
		if color == "green":
			for i in range(self.GUI.dim*self.GUI.dim):
				if board[i] == 'O': # generate valid moves for that piece
					self.allValMoves.update(self.getValidMoves(i, board))
		else:
			for i in range(self.GUI.dim*self.GUI.dim):
				if board[i] == 'X': # generate valid moves for that piece
					self.allValMoves.update(self.getValidMoves(i, board))
		return self.allValMoves
		
	def getValidMoves(self, pos, board):
		#X = pos % self.GUI.dim 			# converts indice to X-coord
		#Y = pos // self.GUI.dim			# converts indice to Y-coord
		coord = (pos % self.GUI.dim, pos // self.GUI.dim)		# 2-tuple for the coord (X,Y)
		valMoves = []					# List to store all valid coordinates(X,Y) at
		jumpList = []

		# check to see if all adjacent moves are valid
		for j in self.adjPos:
			newCoord = (coord[0] + j[0], coord[1] + j[1]) # gets the actual adjacent coordinates
			jumpCoord = (coord[0] + (j[0] * 2), coord[1] + (j[1] * 2))
			
			#newIndice = newCoord[0] + newCoord[1] * self.GUI.dim

			# checks if the adjacent X position is in bounds
			if newCoord[0] >= 0 and newCoord[0] < self.GUI.dim:
				# checks if the adjacent Y position is in bounds
				if newCoord[1] >= 0 and newCoord[1] < self.GUI.dim:
					#  if the position is blank (no piece is there)
					if board[newCoord[0] + newCoord[1] * self.GUI.dim] == ' ':
						# add that position to the list of valid positions
						valMoves.append(newCoord)
					if board[newCoord[0] + newCoord[1] * self.GUI.dim] != ' ':
						if jumpCoord[0] >= 0 and jumpCoord[0] < self.GUI.dim and jumpCoord[1] >= 0 and jumpCoord[1] < self.GUI.dim:
							if board[jumpCoord[0] + jumpCoord[1] * self.GUI.dim] == ' ':
								jumpList.append(jumpCoord)

		# check if there are any jumps for the initial piece passed in
		jumps = self.getJumps(coord, [], board)
		if jumps != None:
			valMoves = valMoves + jumps
		#print("jumps: ", self.coord, ":", self.jumps)
		
		validatedMoves = []		#Filters moves based on whether they follow territory rules
		for move in valMoves:
			if self.territoryConflict(self.GUI.coordToIndice(coord), self.GUI.coordToIndice(move), board):
				continue
			validatedMoves.append(move)
		return {coord: validatedMoves} 	#returns valid positions for one piece to move to
		
	# @ params: takes in the position you want to jump to, and the list of seen positions
	# returns a list of valid positions something can jump to.
	def getJumps(self, pos, seen, board):
		valJumps = [] # keeps track of valid jump positions.
		newSeen = seen  # new seen list to add any valid jumps we visit to

		for z in range(0,8):
			#newAdjX = pos[0] + self.adjPos[z][0]
			#newAdjY = pos[1] + self.adjPos[z][1]
			newAdjCoord = (pos[0] + self.adjPos[z][0], pos[1] + self.adjPos[z][1])

			#adjIndic = newAdjCoord[0] + newAdjCoord[1]*self.GUI.dim


			#jumpX = pos[0] + self.adjJumps[z][0]  # gets the jump X value
			#jumpY = pos[1] + self.adjJumps[z][1]  # gets the jump Y value
			jumpCoord = (pos[0] + self.adjJumps[z][0], pos[1] + self.adjJumps[z][1]) # makes tuple for the X,Y for the jump coord

			# convert new jump (X,Y) to an indice
			#jIndice = jumpCoord[0] + jumpCoord[1] * self.GUI.dim


			# check if jumpcoord is in bounds
			if jumpCoord[0] >= 0 and jumpCoord[0] < self.GUI.dim:
				if jumpCoord[1] >= 0 and jumpCoord[1] < self.GUI.dim:
					# and not in list of seen positions.
					if jumpCoord not in seen:
						# if there is a piece before the jump
						if board[newAdjCoord[0] + newAdjCoord[1]*self.GUI.dim] != ' ':
							# and the spot we want to jump to is not occupied by a piece, add to valid moves
							if board[jumpCoord[0] + jumpCoord[1] * self.GUI.dim] == " ":
								valJumps.append(jumpCoord)
								newSeen.append(jumpCoord)

		# recursively find any more jump positions, update seen to have the place we just jumped to
		for valJump in valJumps:
			valJumps = valJumps + self.getJumps(valJump, newSeen, board)

		if valJumps != None:
			return valJumps
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
				
	def gameWon(self, board, color):	#Detects if a side wins
		if color == "green":
			for i in range(self.GUI.dim//2):
				for j in range(self.GUI.dim//2 + i, self.GUI.dim):
					if board[i * self.GUI.dim + j] != 'O':
						return False
		elif color == "red":
			for i in range(self.GUI.dim//2, self.GUI.dim):
				for j in range(i - self.GUI.dim//2 + 1):
					if board[i * self.GUI.dim + j] != 'X':
						return False
		return True
		
