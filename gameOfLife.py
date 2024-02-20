from random import random as random
from PIL import Image as pimage
from PIL import ImageTk as pimageTK
import time
import tkinter
import os

t = (2, 3)

class cell():
    def __init__(self):
        self.state = (random() < 0.5)
        self.bufferState = False
        self.neighbours = []
    
    def append(self, neighbour):
        self.neighbours.append(neighbour)
    
    def tick(self):
        count = 0
        for neighbour in self.neighbours:
            if neighbour.state:
                count += 1
        if self.state:
            if not (count in t):
                self.bufferState = False
                #self.state = False
        else:
            if count == 3:
                self.bufferState = True
                #self.state = True

class board():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cells = []
        self.img = pimage.new("RGBA", (x, y))
        for i in range(x):
            row = []
            for j in range(y):
                row.append(cell())
            self.cells.append(row)
        for i in range(x):
            for j in range(y):
                mycell = self.cells[i][j]
                if i > 0:
                    mycell.append(self.cells[i - 1][j])
                    if j > 0:
                        mycell.append(self.cells[i - 1][j - 1])
                    if j < y - 1:
                        mycell.append(self.cells[i - 1][j + 1])
                if i < x - 1:
                    mycell.append(self.cells[i + 1][j])
                    if j > 0:
                        mycell.append(self.cells[i + 1][j - 1])
                    if j < y - 1:
                        mycell.append(self.cells[i + 1][j + 1])
                if j > 0:
                    mycell.append(self.cells[i][j - 1])
                if j < y - 1:
                    mycell.append(self.cells[i][j + 1])
                if mycell.state:
                    self.img.putpixel((i, j), (255, 255, 255, 255))
                else:
                    self.img.putpixel((i, j), (0, 0, 0, 255))
    
    def tick(self):
        for i in range(self.x):
            row = self.cells[i]
            for j in range(self.y):
                mycell = row[j]
                mycell.tick()
        for i in range(self.x):
            row = self.cells[i]
            for j in range(self.y):
                mycell = row[j]
                mycell.state = mycell.bufferState
                if mycell.state:
                    self.img.putpixel((i, j), (255, 255, 255, 255))
                else:
                    self.img.putpixel((i, j), (0, 0, 0, 255))

class App(tkinter.Label):
    def __init__(self, x, y):
        self.runBool = True
        
        self.root = tkinter.Tk()
        self.root.configure(background = "black")
        self.root.title("John Conway's Game of Life")
        self.root.resizable(height = False, width = False)
        self.root.grab_set()
        
        super().__init__(self.root, width = x, height = y)
        self.pack()
        
        self.board = board(x, y)
        
        self.root.bind("<Return>", self.run)
        self.root.bind("a", self.tick)
        self.root.bind("<Escape>", self.exit)
        
        self.update()
    
    def update(self):
        icon = pimageTK.PhotoImage(self.board.img)
        self.image = icon
        self.config(image = icon)
        super().update()
        self.root.update()
    
    def tick(self, s = None):
        self.board.tick()
        self.update()
    
    def run(self, s = None):
        self.root.bind("<Return>", lambda s: self.__setattr__("runBool", False))
        while self.runBool:
            self.tick()
        self.runBool = True
        self.root.bind("<Return>", self.run)
    
    def exit(self, s = None):
        self.root.destroy()
        self.root.quit()

while True:
    try:
        os.system("cls")
        print("After starting new Game, click on the rendered frame and press: \n    -\"a\" for tick\n    -ENTER for auto-tick toggle \n    -ESCAPE for exit\n")
        w = int(input("Enter Width  (in Pixel): "))
        h = int(input("Enter Height (in Pixel): "))
        a = App(w, h)
        a.root.mainloop()
    except Exception as e:
        pass