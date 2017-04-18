import tkinter
import time
import sys
from tkinter import *

class HalmaGUI:

	def __init__(self, screen, dim):
		self.board = []
		self.screen = screen
		self.statusText = StringVar()
		self.statusText.set("The game has begun")
		self.status = Label(screen, textvariable = self.statusText, justify = CENTER, relief = RIDGE, width = 25)
		self.status.grid(row = 0, columnspan = dim, pady = 5)
		for i in range(dim):
			for j in range(dim):
				if(i + j + 2 <= dim/2 + 1):
					self.board.append(['X', self.createButton(i, j, "red")])
				elif(i + j + 2 >= dim*1.5 + 1):
					self.board.append(['O', self.createButton(i, j, "blue")])
				else:
					self.board.append([' ', self.createButton(i, j, "")])
				
		tkinter.Button(screen, text = "QUIT", command = self.quit, relief = GROOVE)\
			.grid(row = dim + 1, columnspan = dim, ipadx = 15, ipady = 3, pady = 5)

	def createButton(self, i, j, color):
		tempButton = Canvas(self.screen, borderwidth = 2, relief = GROOVE, width = 10, height = 23)
		tempButton.grid(row = i+1, column = j, ipadx = 12, ipady = 5, padx = 2, pady = 2)
		tempButton.create_oval(7, 7, 33, 33, fill = color, outline = color)
		
		tempButton.bind("<ButtonPress-1>", self.updateLabel)
		tempButton.bind("<ButtonPress-1>", self.push, add="+")
		tempButton.bind("<ButtonRelease-1>", self.release)
		return tempButton
			
	def push(self, event):
		event.widget.configure(relief = SUNKEN)
	
	def release(self, event):
		event.widget.configure(relief = GROOVE)
	
	def updateLabel(self, event):
		self.statusText.set("A button has been clicked!")
		self.screen.after(1000, self.resetLabel)
	
	def resetLabel(self):
		self.statusText.set("Back to business")

	def refreshBoard(self):
		pass
		
	def quit(self):
		self.screen.destroy()


screen = tkinter.Tk(className = "Halma GUI")
theGUI = HalmaGUI(screen, int(sys.argv[1]))
screen.mainloop()