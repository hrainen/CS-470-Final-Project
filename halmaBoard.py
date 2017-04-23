import tkinter
import time
import sys
from tkinter import *

class HalmaGUI:

	def __init__(self, screen, dim, inputFile):
		self.board = []			#This is the list that will hold our halma board
		self.screen = screen	#This is the window the GUI will go in
		self.moveStarted = False
		self.selectedPiece = None
		self.movedPieces = [None, None]
		self.dim = dim
		self.statusText = StringVar()	#This is the status text at the top of the GUI
		self.statusText.set("Select a piece to move")	#Initially set status to "The game has begun"
		#Create status text, pass in self.statusText variable
		self.status = Label(screen, textvariable = self.statusText, justify = CENTER, relief = RIDGE, width = 25)
		#Add status text to GUI using grid() layout, it should be centered along the top of the halma grid
		self.status.grid(row = 0, column = 0, pady = 5)
		
		self.buttonContainer = Canvas(self.screen)
		self.buttonContainer.grid(row = 1, column = 0)
		
		if(inputFile == None):
			self.createBoard()
		else:
			self.loadFromFile(inputFile)
		
		tkinter.Button(screen, text = "SAVE BOARD", command = self.saveModal, relief = GROOVE)\
			.grid(row = 2, column = 0, ipadx = 15, ipady = 3, pady = 5)
		
		#Add quit button to bottom of GUI, centered along halma grid
		tkinter.Button(screen, text = "QUIT", command = self.quit, relief = GROOVE)\
			.grid(row = 3, column = 0, ipadx = 15, ipady = 3, pady = 5)

		tkinter.Button(screen, text="genMovesTest", command=self.genMovesRed, relief=GROOVE) \
			.grid(row=4, column=0, ipadx=15, ipady=3, pady=5)

	def createBoard(self):
		#For loop to create buttons that make up halma board (dim^2 total)
		for i in range(self.dim):
			for j in range(self.dim):
				if(i + j + 2 <= self.dim/2 + 1):		#If top left corner, create button with red piece
					self.board.append(['X', self.createButton(i, j, "red")])
				elif(i + j + 2 >= self.dim*1.5 + 1):	#If bottom right, create button with blue piece
					self.board.append(['O', self.createButton(i, j, "blue")])
				else:							#Else, create blank button (or blank halma square)
					self.board.append([' ', self.createButton(i, j, "")])
		self.createWinRegions()

	''' I think i know what to do for restricting movement for a player,
		when we get the turn taking working, just find valid moves for
		whos turn it is, more on this later '''


	# @ params: No params for now
	# returns a dictionary where the key is the piece we want to move,
	# 					   and the value is a list of valid positions for that piece to move to
	def genMovesRed(self):
		self.allValMoves = {} 		# append dictionaries for pieces and their valid moves here

		# loop through the board, if the piece being checked belongs to the player whos moves we're generating
		for i in range(self.dim*self.dim):
			if self.board[i][0] == "X": # generate valid moves for that piece
				self.allValMoves.update(self.getValidMoves(i))
		print(self.allValMoves)


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
			self.valMoves + list(self.jumps)
		print("jumps: ", self.coord, ":", self.jumps)


		return {self.coord: self.valMoves} 	#returns valid positions for one piece to move to
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

		#coords of potential adjacent jumps
		self.adjJumps = [(-2, -2), (0, -2), (2, -2),
						 (-2, 0), 			(2, 0),
						 (-2, 2), (0, 2),   (2, 2)]

		# the coordinates of adjacent squares
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

		# recursively find any more jump positions, update seen to have the place we just jumped to

		if self.valJumps != None:
			return self.valJumps
		else:
			return None



	def loadFromFile(self, inputFile):
		j = 0
		fileID = open(inputFile, 'r')
		for i in range(self.dim):
			row = fileID.readline().split( )
			for letter in row:
				if letter == 'X':
					self.board.append(['X', self.createButton(i, j, "red")])
				elif letter == 'O':
					self.board.append(['O', self.createButton(i, j, "blue")])
				elif letter == '_':
					self.board.append([' ', self.createButton(i, j, "")])
				j += 1
			j = 0
		fileID.close()
		self.createWinRegions()
	
	def saveToFile(self, inputModal, outputFile):
		i = 0
		fileID = open(outputFile, 'w')
		for position in self.board:
			if position[0] == ' ':
				fileID.write("_")
			elif position[0] == 'X':
				fileID.write("X")
			elif position[0] == 'O':
				fileID.write("O")
			
			if i + 1 == self.dim:
				i = -1
				fileID.write("\n")
			else:
				fileID.write(" ")
			i += 1
		fileID.close()
		print("Saved board to: " + outputFile)
		self.quitModal(inputModal)
			
	def saveModal(self):
		saveModal = Toplevel()
		
		label = Label(saveModal, text = "File to save: ", justify = LEFT, relief = RIDGE, width = 25)
		label.grid(row = 0, column = 0, pady = 5)
		
		entry = Entry(saveModal, justify = LEFT, relief = RIDGE, width = 25)
		entry.grid(row = 0, column = 1, pady = 5)
		
		tkinter.Button(saveModal, text = "SAVE", command = lambda: self.saveToFile(saveModal, entry.get()), relief = GROOVE)\
			.grid(row = 1, column = 0, ipadx = 15, ipady = 3, pady = 5)
			
		tkinter.Button(saveModal, text = "CANCEL", command = lambda: self.quitModal(saveModal), relief = GROOVE)\
			.grid(row = 1, column = 1, ipadx = 15, ipady = 3, pady = 5)
		
		saveModal.transient(self.screen)
		saveModal.grab_set()
		self.screen.wait_window(saveModal)
	
	def createWinRegions(self):
		#Y start = 45, increment 45
		#X start = 46, increment 46
		for i in range(0, self.dim//2):	#Draw upper left zone
			self.buttonContainer.create_line(46*i, 45*(self.dim/2 - i), 46*(i + 1), 45*(self.dim/2 - i), width = 4)
			self.buttonContainer.create_line(46*(i + 1), 45*(self.dim/2 - i), 46*(i + 1), 45*(self.dim/2 - i - 1), width = 4)
		for i in range(0, self.dim//2):	#Draw bottom right zone
			self.buttonContainer.create_line(46*(self.dim - i), 45*(self.dim/2 + i), 46*(self.dim - i - 1), 45*(self.dim/2 + i), width = 4)
			self.buttonContainer.create_line(46*(self.dim - i - 1), 45*(self.dim/2 + i), 46*(self.dim - i - 1), 45*(self.dim/2 + i + 1), width = 4)
		
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
		self.refreshBoard()			#Update board to show changes
	
	def resetLabel(self):
		self.statusText.set("Select a piece to move")
	
	def moveSelectedPiece(self, piece):	#Moves selectedPiece to the given piece location
		piece[0] = self.selectedPiece[0]
		self.selectedPiece[0] = ' '
		self.movedPieces = [piece, self.selectedPiece]
		self.selectedPiece = None	#Deselect space, as there are no pieces there anymore
		if self.gameWon():
			self.disableBoard()
		else:
			self.statusText.set("A piece has been moved!")
			self.screen.after(2000, self.resetLabel)

	def refreshBoard(self):	#Updates halma piece positions, and visuals
		for piece in self.board:	#Clear board
			piece[1].delete("all")
		
		if self.selectedPiece != None:	#Mark selected pieces with green rectangle
			self.selectedPiece[1].create_rectangle(0, 0, 36, 35, fill = "green", outline = "green")
			
		if self.movedPieces[0] != None and self.movedPieces[1] != None:	#Mark spaces involving movement with yellow rectangle
			self.movedPieces[0][1].create_rectangle(0, 0, 36, 35, fill = "yellow", outline = "yellow")
			self.movedPieces[1][1].create_rectangle(0, 0, 36, 35, fill = "yellow", outline = "yellow")
		
		for piece in self.board:	#Mark X with red circle and O with blue circle
			if piece[0] == 'X':
				piece[1].create_oval(7, 7, 33, 33, fill = "red", outline = "red")
			if piece[0] == 'O':
				piece[1].create_oval(7, 7, 33, 33, fill = "blue", outline = "blue")
	
	def gameWon(self):
		winnerO = True
		winnerX = True
		for i in range(self.dim):
			for j in range(self.dim):
				if(i + j + 2 <= self.dim/2 + 1):		#If top left corner, create button with red piece
					if self.board[i * self.dim + j][0] != 'O':
						winnerO = False
				elif(i + j + 2 >= self.dim*1.5 + 1):	#If bottom right, create button with blue piece
					if self.board[i * self.dim + j][0] != 'X':
						winnerX = False
		if winnerO and winnerX:
			self.statusText.set("Both sides won...somehow")
			return True
		elif winnerX:
			self.statusText.set("Team Red Wins!")
			return True
		elif winnerO:
			self.statusText.set("Team Blue Wins!")
			return True
		else:
			return False
	
	def disableBoard(self):
		for button in self.board:
			button[1].bind("<ButtonPress-1>", self.push)
	
	def quitModal(self, inputModal):
		inputModal.destroy()
	
	def quit(self):	#Quit GUI
		self.screen.destroy()


screen = tkinter.Tk(className = "Halma GUI")	#Create window for GUI
if len(sys.argv) == 2:
	theGUI = HalmaGUI(screen, int(sys.argv[1]), None)	#Create HalmaGUI object, pass in window and dimensions
elif len(sys.argv) == 3:
	theGUI = HalmaGUI(screen, int(sys.argv[1]), sys.argv[2])	#Create HalmaGUI object, pass in window, dimensions, and input file
else:
	print ("""You must run the program with one of two commands:
	1. python halmaBoard.py dimensions
	2. python halmaBoard.py dimensions inputFile.txt""")
	sys.exit()
screen.mainloop()	#Run GUI
