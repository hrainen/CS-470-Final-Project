import tkinter
import time
import sys
from tkinter import *
from projectTBD import ProjectTBD

class HalmaGUI:

	def __init__(self, screen, dim, computerColor, inputFile):
		self.board = []			#This is the list that will hold our halma board
		self.screen = screen	#This is the window the GUI will go in
		self.selectedPiece = None	#This will hold a selected piece
		self.movedPieces = [None, None]		#This holds recently moved positions
		self.computer = None
		self.continueComp = True
		self.computerColor = computerColor
		self.dim = dim						#Holds board dimensions
		self.statusText = StringVar()	#This is the status text at the top of the GUI
		
		#Create status text, pass in self.statusText variable
		self.status = Label(screen, textvariable = self.statusText, justify = CENTER, relief = RIDGE, width = 40)
		#Add status text to GUI using grid() layout, it should be centered along the top of the halma grid
		self.status.grid(row = 0, column = 0, pady = 5)
		
		self.buttonContainer = Canvas(self.screen)	#Create canvas to hold game board
		self.buttonContainer.grid(row = 1, column = 0)	#Put right after status

		self.playerTurn = "O"	#Green always goes first

		if(inputFile == None):	#If no input file, create new board
			self.createBoard()
		else:					#If there is an input file, load board from file
			self.loadFromFile(inputFile)
		
		self.addLabels()		#Add labels to board
		
		scoreText = self.getScore()
		self.statusText.set("Select a piece to move. Scores: (%s)" % (' '.join(str(x) for x in scoreText)))	#Initially set status
		
		#Add button activate save modal, so that user can save board
		tkinter.Button(screen, text = "SAVE BOARD", command = self.saveModal, relief = GROOVE)\
			.grid(row = 2, column = 0, ipadx = 15, ipady = 3, pady = 5)
		
		#Add quit button to bottom of GUI, centered along halma grid
		tkinter.Button(screen, text = "QUIT", command = self.quit, relief = GROOVE)\
			.grid(row = 3, column = 0, ipadx = 15, ipady = 3, pady = 5)

		#Add buttons to test gen moves
		#tkinter.Button(screen, text="genMovesTestRed", command=self.genMovesRed, relief=GROOVE) \
		#	.grid(row=4, column=0, ipadx=15, ipady=3, pady=5)

		#tkinter.Button(screen, text="genMovesTestGreen", command=self.genMovesGreen, relief=GROOVE) \
		#	.grid(row=5, column=0, ipadx=15, ipady=3, pady=5)

		#Add button to test indices
		#tkinter.Button(screen, text="Indice Text", command=self.printindice, relief=GROOVE) \
		#	.grid(row=6, column=0, ipadx=15, ipady=3, pady=5)

	def configureComputer(self, computer):	#Puts computer AI into global variable
		self.computer = computer
		#Query computer for a move on its turn
		if (self.playerTurn == "O" and self.computer.color == "green") or (self.playerTurn == "X" and self.computer.color != "green")\
			and self.continueComp:
			self.statusText.set("The computer is thinking...")
			self.screen.after(500, self.computer.calculateMove)
		
	def createBoard(self):
		#For loop to create buttons that make up halma board (dim^2 total)
		self.counter = 0

		for i in range(self.dim):
			for j in range(self.dim):
				if(self.inTopRight(i, j)):		#If top right corner, create button with red piece
					self.board.append(['X', self.createButton(i, j, "red"), self.counter])

				elif(self.inBottomLeft(i, j)):	#If bottom left, create button with green piece
					self.board.append(['O', self.createButton(i, j, "green"), self.counter])

				else:							#Else, create blank button (or blank halma square)
					self.board.append([' ', self.createButton(i, j, ""), self.counter])

				self.counter += 1
		self.createWinRegions()	#Draw win regions, or territory boundaries

	''' I think i know what to do for restricting movement for a player,
		when we get the turn taking working, just find valid moves for
		whos turn it is, more on this later '''

	def coordToIndice(self, coord):		#Convert coordinates to the proper index
		return coord[0] + self.dim*coord[1]

	def indiceToCoord(self, indice):	#Convert an index to the proper coordinates
		x = indice % self.dim
		y = indice // self.dim
		return (x,y)

	def printindice(self):				#Print index for testing
		for x in self.board:
			print(x[2])

	# @ params: No params for now
	# returns a dictionary where the key is the piece we want to move,
	# 					   and the value is a list of valid positions for that piece to move to
	def genMovesRed(self):
		self.allValMoves = {} 		# append dictionaries for pieces and their valid moves here

		# loop through the board, if the piece being checked belongs to the player whos moves we're generating
		for i in range(self.dim*self.dim):
			if self.board[i][0] == "X": # generate valid moves for that piece
				self.allValMoves.update(self.getValidMoves(i))
		return self.allValMoves

	def genMovesGreen(self):
		self.allValMoves = {} 		# append dictionaries for pieces and their valid moves here

		# loop through the board, if the piece being checked belongs to the player whos moves we're generating
		for i in range(self.dim*self.dim):
			if self.board[i][0] == "O": # generate valid moves for that piece
				self.allValMoves.update(self.getValidMoves(i))
		return self.allValMoves


	# @ params: takes in position(list index) for the piece we want to find valid moves for
	# returns a dictionary {key: value} where the key is the initial position passed in,
	# 					   and the value is a list of valid positions for the initial coord to move to
	def getValidMoves(self, pos):
		self.X = pos % self.dim 			# converts indice to X-coord
		self.Y = pos // self.dim			# converts indice to Y-coord
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

			self.newIndice = self.newCoord[0] + self.newCoord[1]*self.dim


			# checks if the adjacent X position is in bounds
			if self.newX >= 0 and self.newX < self.dim:
				# checks if the adjacent Y position is in bounds
				if self.newY >= 0 and self.newY < self.dim:
					#  if the position is blank (no piece is there)
					if self.board[self.newIndice][0] == " ":
						# add that position to the list of valid positions
						self.valMoves.append(self.newCoord)
					"""
					# else, there is a piece there (red or blue) doesnt matter whos, you might be able to jump from there
					else:
						# get the position we want to jump to
						self.jumpToX = self.X + j[0]*2
						self.jumpToY = self.Y + j[1]*2
						self.jumpToCoord = (self.jumpToX, self.jumpToY)

						# call getJumps and append any valid jumps to the list of valid jumps
						self.jumps = self.getJumps(self.jumpToCoord, [])
						if self.jumps != None:
							self.valMoves += self.jumps
							print("jumps: ", self.coord, ":", self.jumps)
					"""

		# check if there are any jumps for the initial piece passed in
		self.jumps = list(self.getJumps(self.coord, []))
		if self.jumps != None:
			self.valMoves = self.valMoves + list(self.jumps)
		#print("jumps: ", self.coord, ":", self.jumps)
		
		validatedMoves = []		#Filters moves based on whether they follow territory rules
		for move in self.valMoves:
			if self.territoryConflict(self.board[self.coordToIndice(self.coord)], self.board[self.coordToIndice(move)]):
				continue
			validatedMoves.append(move)
		return {self.coord: validatedMoves} 	#returns valid positions for one piece to move to
	"""
	def getJumps(self, jpos, seen):
		# list of valid jumps to return
		self.validJumps = []

		# convert jpos into indice
		self.jIndice = jpos[0] + jpos[1]*self.dim

		# check if jump is in bounds
		if jpos[0] >= 0 and jpos[0] < self.dim:
			if jpos[1] >= 0 and jpos[1] < self.dim:
				# and not in list of seen positions.
				if jpos not in seen:
					# and the spot we want to jump to is not occupied by a piece, add to valid moves
					if self.board[self.jIndice][0] == " ":
						self.validJumps.append(jpos)
						return self.validJumps

		return None
	"""

	# @ params: takes in the position you want to jump to, and the list of seen positions
	# returns a list of valid positions something can jump to.
	def getJumps(self, pos, seen):
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

			self.adjIndic = self.newAdjCoord[0] + self.newAdjCoord[1]*self.dim


			self.jumpX = pos[0] + self.adjJumps[z][0]  # gets the jump X value
			self.jumpY = pos[1] + self.adjJumps[z][1]  # gets the jump Y value
			self.jumpCoord = (self.jumpX, self.jumpY) # makes tuple for the X,Y for the jump coord

			# convert new jump (X,Y) to an indice
			self.jIndice = self.jumpCoord[0] + self.jumpCoord[1] * self.dim


			# check if jumpcoord is in bounds
			if self.jumpX >= 0 and self.jumpX < self.dim:
				if self.jumpY >= 0 and self.jumpY < self.dim:
					# and not in list of seen positions.
					if self.jumpCoord not in seen:
						# if there is a piece before the jump
						if self.board[self.adjIndic][0] != " ":
							# and the spot we want to jump to is not occupied by a piece, add to valid moves
							if self.board[self.jIndice][0] == " ":
								self.valJumps.append(self.jumpCoord)
								self.newSeen.append(self.jumpCoord)

		# recursively find any more jump positions, update seen to have the place we just jumped to
		for valJump in self.valJumps:
			self.valJumps = self.valJumps + list(self.getJumps(valJump, self.newSeen))

		if self.valJumps != None:
			return self.valJumps
		else:
			return None

	def loadFromFile(self, inputFile):	#Load halma board from file
		j = 0
		self.counter = 0
		fileID = open(inputFile, 'r')	#Open file to read
		for i in range(self.dim):		#Add pieces to board based on characters received from file
			row = fileID.readline().split( )
			for letter in row:
				if letter == 'X':		#Add red piece
					self.board.append(['X', self.createButton(i, j, "red"), self.counter])

				elif letter == 'O':		#Add green piece
					self.board.append(['O', self.createButton(i, j, "green"), self.counter])

				elif letter == '_':		#Add empty space
					self.board.append([' ', self.createButton(i, j, ""), self.counter])
				self.counter += 1
				j += 1
			j = 0
		fileID.close()					#Close file
		self.createWinRegions()			#Draw win regions, or territory boundaries
	
	def addLabels(self):	#Add labels (1, 2, 3...) and (a, b, c, ...)
		for i in range(self.dim):
			Label(self.buttonContainer, text = i + 1, justify = CENTER)\
			.grid(row = i + 1, column = self.dim + 1, ipadx = 5, ipady = 5, padx = 0, pady = 2)
		for i in range(self.dim):
			Label(self.buttonContainer, text = chr(i + 1 + 96), justify = CENTER)\
			.grid(row = self.dim + 2, column = i, ipadx = 5, ipady = 5, padx = 0, pady = 2)
	
	def saveToFile(self, inputModal, outputFile):	#Save board to specified file
		i = 0
		fileID = open(outputFile, 'w')	#Open file to write to
		for position in self.board:		#Go through board array, and print corresponding values to file
			if position[0] == ' ':		#Blank spaces are denoted as "_"
				fileID.write("_")
			elif position[0] == 'X':
				fileID.write("X")
			elif position[0] == 'O':
				fileID.write("O")
			
			if i + 1 == self.dim:		#New line for each row
				i = -1
				fileID.write("\n")
			else:						#Space between columns
				fileID.write(" ")
			i += 1
		fileID.close()					#Close file written to
		print("Saved board to: " + outputFile)
		self.quitModal(inputModal)		#Quit save modal
			
	def saveModal(self):	#Spawn save modal for user to utilize
		saveModal = Toplevel()	#Put modal on top level
		
		#Prompt user to input save file location
		label = Label(saveModal, text = "File to save: ", justify = LEFT, relief = RIDGE, width = 25)
		label.grid(row = 0, column = 0, pady = 5)
		
		#Create text field for user to put file location in
		entry = Entry(saveModal, justify = LEFT, relief = RIDGE, width = 25)
		entry.grid(row = 0, column = 1, pady = 5)
		
		#Save board to specified file location and quit
		tkinter.Button(saveModal, text = "SAVE", command = lambda: self.saveToFile(saveModal, entry.get()), relief = GROOVE)\
			.grid(row = 1, column = 0, ipadx = 15, ipady = 3, pady = 5)
		
		#Quit save modal
		tkinter.Button(saveModal, text = "CANCEL", command = lambda: self.quitModal(saveModal), relief = GROOVE)\
			.grid(row = 1, column = 1, ipadx = 15, ipady = 3, pady = 5)
		
		#Initialize saveModal
		saveModal.transient(self.screen)
		saveModal.grab_set()
		self.screen.wait_window(saveModal)
	
	def createWinRegions(self):
		#Y start = 45, increment 45
		#X start = 46, increment 46
		for i in range(0, self.dim//2):		#Draw bottom left zone
			self.buttonContainer.create_line(46*i, 45*(self.dim/2 + i), 46*(i + 1), 45*(self.dim/2 + i), width = 4)
			self.buttonContainer.create_line(46*(i + 1), 45*(self.dim/2 + i), 46*(i + 1), 45*(self.dim/2 + i + 1), width = 4)
		for i in range(0, self.dim//2):		#Draw upper right zone
			self.buttonContainer.create_line(46*(self.dim - i), 45*(self.dim/2 - i), 46*(self.dim - i - 1), 45*(self.dim/2 - i), width = 4)
			self.buttonContainer.create_line(46*(self.dim - i - 1), 45*(self.dim/2 - i), 46*(self.dim - i - 1), 45*(self.dim/2 - i - 1), width = 4)
		
	def createButton(self, i, j, color):	#Create a custom button using Canvas()
		#Create initial button appearance (does nothing when clicked)
		tempButton = Canvas(self.buttonContainer, borderwidth = 2, relief = GROOVE, width = 10, height = 23)
		tempButton.grid(row = i+1, column = j, ipadx = 12, ipady = 5, padx = 2, pady = 2)
		
		#Draw type of circle, depending on button location
		tempButton.create_oval(7, 7, 33, 33, fill = color, outline = color)
		
		#Add bindings for when the button is pressed and released
		#Includes different relief states when pressed and released
		tempButton.bind("<ButtonPress-1>", self.updateLabel)
		#Add lets us use another binding for ButtonPress-1
		tempButton.bind("<ButtonPress-1>", self.push, add="+")
		tempButton.bind("<ButtonRelease-1>", self.release)
		return tempButton
			
	def push(self, event):	#Set button to SUNKEN to simulate button press
		event.widget.configure(relief = SUNKEN)
	
	def release(self, event):	#Set button back to normal GROOVE state after release
		event.widget.configure(relief = GROOVE)
	
	def updateLabel(self, event):	#Update label, reset after 1 second
		self.movedPieces = [None, None]		#Reset spaces involving movement
		for piece in self.board:			#Iterate through board, and find space clicked
			if piece[1] == event.widget and self.selectedPiece == None:	#If space found, and currently no selected pieces
				if piece[0] != ' ':		#If space contains a piece, select that piece!
					self.statusText.set("A gamepiece has been selected!")
					self.selectedPiece = piece
			#If space found, and it contains the currently selected piece, deselect it
			elif piece[1] == event.widget and piece[1] == self.selectedPiece[1]:
				self.selectedPiece = None
				self.statusText.set("A gamepiece has been deselected")
			#If space found, and a piece has already been selected
			elif piece[1] == event.widget and self.selectedPiece != None:
				if piece[0] != ' ':	#If space contains a piece, tell user that space is occupied
					self.statusText.set("That space is currently occupied")
				else:				#If space is empty, move selected piece to that location!
					self.moveSelectedPiece(piece)
					#Query computer for a move on its turn
					if (self.playerTurn == "O" and self.computer.color == "green") or (self.playerTurn == "X" and self.computer.color != "green")\
						and self.continueComp:
						self.statusText.set("The computer is thinking...")
						self.screen.after(500, self.computer.calculateMove)
		self.refreshBoard()			#Update board to show changes
	
	def resetLabel(self):	#Generic text to guide user to action
		self.statusText.set("Select a piece to move")
	
	def moveSelectedPiece(self, piece):	#Moves selectedPiece to the given piece location
		# generate valid move positions for this piece, and
		self.valMovesSelect = self.getValidMoves(self.selectedPiece[2])
		# if the location it wants to move to is in the list of valid moves, and no territory conflicts arise
		if self.indiceToCoord(piece[2]) in self.valMovesSelect[self.indiceToCoord(self.selectedPiece[2])]:
			# and the piece selected belongs to the player whos turn it is
			if self.selectedPiece[0] == self.playerTurn:
				# Then move the piece there
				piece[0] = self.selectedPiece[0]
				self.selectedPiece[0] = ' '
				self.movedPieces = [piece, self.selectedPiece]
				self.selectedPiece = None	#Deselect space, as there are no pieces there anymore
				if self.gameWon():
					self.disableBoard()
				else:
					scoreText = self.getScore()
					self.statusText.set("A piece has been moved! ("\
						+ str(self.movedPieces[1][2]//self.dim + 1) + "," + chr(self.movedPieces[1][2]%self.dim + 97) + ")->("\
						+ str(self.movedPieces[0][2]//self.dim + 1) + "," + chr(self.movedPieces[0][2]%self.dim + 97) + ")"\
						+ " Scores: (%s)" % (' '.join(str(x) for x in scoreText)))
				# Update self.playerTurn to be the opponents turn
				if self.playerTurn == "O":
					self.playerTurn = "X"
				else:
					self.playerTurn = "O"
				
			else:# update label to say it is not that players turn
				self.statusText.set("It is not your turn to move!")
		else:
			# player has selected correct piece for their turn, but has selected an invalid spot to move to
			if self.selectedPiece[0] == self.playerTurn:
				print(self.valMovesSelect)
				self.statusText.set("Not a valid move ("\
					+ str(self.selectedPiece[2]//self.dim + 1) + "," + chr(self.selectedPiece[2]%self.dim + 97) + ")->("\
					+ str(piece[2]//self.dim + 1) + "," + chr(piece[2]%self.dim + 97) + ")")

			# player has selected the wrong piece for their turn, tell them its the other players turn to move.
			else:
				self.statusText.set("It is not your turn to move!")
	
	def territoryConflict(self, start, end):	#Checks to see if a player is trying an illegal move concerning territories
		#If green is in enemy territory, it cannot move back out
		if start[0] == 'O' and self.inTopRight(start[2]//self.dim, start[2]%self.dim):
			if not self.inTopRight(end[2]//self.dim, end[2]%self.dim):
				return True
		#If green is outside of its home territory, it may not move back
		elif start[0] == 'O' and not self.inBottomLeft(start[2]//self.dim, start[2]%self.dim):
			if self.inBottomLeft(end[2]//self.dim, end[2]%self.dim):
				return True
		#Same rules as above, except for red
		if start[0] == 'X' and self.inBottomLeft(start[2]//self.dim, start[2]%self.dim):
			if not self.inBottomLeft(end[2]//self.dim, end[2]%self.dim):
				return True
		elif start[0] == 'X' and not self.inTopRight(start[2]//self.dim, start[2]%self.dim):
			if self.inTopRight(end[2]//self.dim, end[2]%self.dim):
				return True
			
	
	def refreshBoard(self):	#Updates halma piece positions, and visuals
		for piece in self.board:	#Clear board
			piece[1].delete("all")
		
		if self.selectedPiece != None:	#Mark selected pieces with blue rectangle
			self.selectedPiece[1].create_rectangle(0, 0, 36, 35, fill = "blue", outline = "blue")
			
		if self.movedPieces[0] != None and self.movedPieces[1] != None:	#Mark spaces involving movement with yellow rectangle
			self.movedPieces[0][1].create_rectangle(0, 0, 36, 35, fill = "yellow", outline = "yellow")
			self.movedPieces[1][1].create_rectangle(0, 0, 36, 35, fill = "yellow", outline = "yellow")
		
		for piece in self.board:	#Mark X with red circle and O with green circle
			if piece[0] == 'X':
				piece[1].create_oval(7, 7, 33, 33, fill = "red", outline = "red")
			if piece[0] == 'O':
				piece[1].create_oval(7, 7, 33, 33, fill = "green", outline = "green")
	
	def genSimpleBoard(self):
		simpleBoard = []
		for piece in self.board:
			simpleBoard.append(piece[0])
		return simpleBoard
	
	def distanceBetweenPoints(self, x, y, a, b):
		return int(((a-x)**2 + (b-y)**2)**(1/2))
	
	def getScore(self):
		totalScore = [0, 0]
		distance = 0
		for i in range(self.dim):
			for j in range(self.dim):
				if self.board[i * self.dim + j][0] == 'O' and not self.inTopRight(i, j):
					for x in range(self.dim//2, self.dim):
						tempDist = self.distanceBetweenPoints(j, i, x, x - self.dim/2)
						if distance == 0 or tempDist < distance:
							distance = tempDist
					totalScore[0] += distance
					distance = 0
				elif self.board[i * self.dim + j][0] == 'X' and not self.inBottomLeft(i, j):
					for x in range(self.dim//2):
						tempDist = self.distanceBetweenPoints(j, i, x, x + self.dim/2)
						if distance == 0 or tempDist < distance:
							distance = tempDist
					totalScore[1] += distance
					distance = 0
		return totalScore
	
	def gameWon(self):	#Detects if a side wins
		winnerO = True
		winnerX = True
		for i in range(self.dim):
			for j in range(self.dim):
				if(self.inTopRight(i, j)):		#If top right corner isn't filled with green, green does not win
					if self.board[i * self.dim + j][0] != 'O':
						winnerO = False
				elif(self.inBottomLeft(i, j)):	#If bottom left corner isn't filled with red, red does not win
					if self.board[i * self.dim + j][0] != 'X':
						winnerX = False
		scoreText = self.getScore()
		if winnerO and winnerX:		#If both sides win, be very confused
			self.statusText.set("Both sides won...somehow. Scores: (%s)" % (' '.join(str(x) for x in scoreText)))
			return True
		elif winnerX:				#If red team wins, update status with good news
			self.statusText.set("Team Red Wins! Scores: (%s)" % (' '.join(str(x) for x in scoreText)))
			return True
		elif winnerO:				#If green team wins, update status with good news
			self.statusText.set("Team Green Wins! Scores: (%s)" % (' '.join(str(x) for x in scoreText)))
			return True
		else:						#If no teams win, return false
			return False
	
	def inTopRight(self, i, j):	#Checks to see if a piece is in the top right of the board
		if(i + self.dim - j + 1 <= self.dim/2 + 1):
			return True
		else:
			return False
		
	def inBottomLeft(self, i, j):	#Checks to see if a piece is in the bottom left of the board
		if(self.dim - i + j + 1 <= self.dim/2 + 1):
			return True
		else:
			return False
	
	def disableBoard(self):			#Disables game board buttons
		for button in self.board:
			button[1].bind("<ButtonPress-1>", self.push)
		self.continueComp = False
	
	def quitModal(self, inputModal):	#Quits a modal
		inputModal.destroy()
	
	def quit(self):	#Quit GUI
		self.screen.destroy()


screen = tkinter.Tk(className = "Halma GUI")	#Create window for GUI
if len(sys.argv) == 4:
	theGUI = HalmaGUI(screen, int(sys.argv[1]), sys.argv[3], None)	#Create HalmaGUI object, pass in window and dimensions
	theMind = ProjectTBD(theGUI, int(sys.argv[2]), sys.argv[3])
	theGUI.configureComputer(theMind)
elif len(sys.argv) == 5:
	theGUI = HalmaGUI(screen, int(sys.argv[1]), sys.argv[3], sys.argv[4])	#Create HalmaGUI object, pass in window, dimensions, and input file
	theMind = ProjectTBD(theGUI, int(sys.argv[2]), sys.argv[3])
	theGUI.configureComputer(theMind)
else:
	print ("""You must run the program with one of two commands:
	1. python halmaBoard.py dimensions time_limit computer_player
	2. python halmaBoard.py dimensions time_limit computer_player inputFile.txt""")
	sys.exit()
screen.mainloop()	#Run GUI
