import tkinter
import time
import sys
from tkinter import *

class HalmaGUI:

	def __init__(self, screen, dim):
		self.board = []			#This is the list that will hold our halma board
		self.screen = screen	#This is the window the GUI will go in
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
		self.statusText.set("A button has been clicked!")
		self.screen.after(1000, self.resetLabel)
	
	def resetLabel(self):	#Reset label
		self.statusText.set("Back to business")

	def refreshBoard(self):	#Right now just skeleton code, should update halma piece positions
		pass
		
	def quit(self):	#Quit GUI
		self.screen.destroy()


screen = tkinter.Tk(className = "Halma GUI")	#Create window for GUI
theGUI = HalmaGUI(screen, int(sys.argv[1]))		#Create HalmaGUI object, pass in window and dimensions
screen.mainloop()								#Run GUI