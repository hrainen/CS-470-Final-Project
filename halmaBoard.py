import tkinter
import time
import sys
from tkinter import *

class HalmaGUI:

	def __init__(self, screen, dim):
		self.board = []			#This is the list that will hold our halma board
		self.screen = screen	#This is the window the GUI will go in
		self.moveStarted = False
		self.selectedPiece = None
		self.movedPieces = [None, None]
		self.statusText = StringVar()	#This is the status text at the top of the GUI
		self.statusText.set("The game has begun")	#Initially set status to "The game has begun"
		#Create status text, pass in self.statusText variable
		self.status = Label(screen, textvariable = self.statusText, justify = CENTER, relief = RIDGE, width = 25)
		#Add status text to GUI using grid() layout, it should be centered along the top of the halma grid
		self.status.grid(row = 0, columnspan = dim, pady = 5)
		
		#For loop to create buttons that make up halma board (dim^2 total)
		for i in range(dim):
			for j in range(dim):
				if(i + j + 2 <= dim/2 + 1):		#If top left corner, create button with red piece
					self.board.append(['X', self.createButton(i, j, "red")])
				elif(i + j + 2 >= dim*1.5 + 1):	#If bottom right, create button with blue piece
					self.board.append(['O', self.createButton(i, j, "blue")])
				else:							#Else, create blank button (or blank halma square)
					self.board.append([' ', self.createButton(i, j, "")])
		
		#Add quit button to bottom of GUI, centered along halma grid
		tkinter.Button(screen, text = "QUIT", command = self.quit, relief = GROOVE)\
			.grid(row = dim + 1, columnspan = dim, ipadx = 15, ipady = 3, pady = 5)

	def createButton(self, i, j, color):	#Create a custom button using Canvas()
		#Create initial button appearance (does nothing when clicked)
		tempButton = Canvas(self.screen, borderwidth = 2, relief = GROOVE, width = 10, height = 23)
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
		self.screen.after(1000, self.resetLabel)	#Reset label at top
	
	def moveSelectedPiece(self, piece):	#Moves selectedPiece to the given piece location
		piece[0] = self.selectedPiece[0]
		self.selectedPiece[0] = ' '
		self.movedPieces = [piece, self.selectedPiece]
		self.selectedPiece = None	#Deselect space, as there are no pieces there anymore
		self.statusText.set("A piece has been moved!")
	
	def resetLabel(self):	#Reset label
		self.statusText.set("Back to business")

	def refreshBoard(self):	#Updates halma piece positions, and visuals
		for piece in self.board:	#Clear board
			piece[1].delete("all")
		
		if self.selectedPiece != None:	#Mark selected pieces with green rectangle
			self.selectedPiece[1].create_rectangle(0, 0, 36, 35, fill = "green", outline = "green")
			
		if self.movedPieces[0] != None and self.movedPieces[1] != None:	#Mark spaces involving movement with yellow rectangle
			self.movedPieces[0][1].create_rectangle(0, 0, 36, 35, fill = "yellow", outline = "yellow")
			self.movedPieces[1][1].create_rectangle(0, 0, 36, 35, fill = "yellow", outline = "yellow")
		
		for piece in self.board:	#Mark X with red circle and Y with blue circle
			if piece[0] == 'X':
				piece[1].create_oval(7, 7, 33, 33, fill = "red", outline = "red")
			if piece[0] == 'O':
				piece[1].create_oval(7, 7, 33, 33, fill = "blue", outline = "blue")
		
	def quit(self):	#Quit GUI
		self.screen.destroy()


screen = tkinter.Tk(className = "Halma GUI")	#Create window for GUI
theGUI = HalmaGUI(screen, int(sys.argv[1]))		#Create HalmaGUI object, pass in window and dimensions
screen.mainloop()								#Run GUI