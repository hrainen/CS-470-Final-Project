import tkinter
import time
from tkinter import *

class HalmaGUI:
	def __init__(self, screen):
		self.screen = screen
		self.statusText = StringVar()
		self.statusText.set("The game has begun")
		self.status = Label(screen, textvariable = self.statusText, justify = CENTER, relief = RIDGE, width = 25)
		self.status.grid(row = 0, columnspan = 8, pady = 5)
		for i in range(8):
			for j in range(8):
				tkinter.Button(screen, text = "", command = self.updateLabel, relief = GROOVE)\
				.grid(row = i+1, column = j, ipadx = 12, ipady = 5, padx = 2, pady = 2)
		tkinter.Button(screen, text = "QUIT", command = self.quit, relief = GROOVE)\
		.grid(row = 9, columnspan = 8, ipadx = 15, ipady = 3, pady = 5)

	def updateLabel(self):
		self.statusText.set("A button has been clicked!")
		self.screen.after(1000, self.resetLabel)
	
	def resetLabel(self):
		self.statusText.set("Back to business")
		
	def quit(self):
		self.screen.destroy()


screen = tkinter.Tk(className = "Halma GUI")
theGUI = HalmaGUI(screen)
screen.mainloop()