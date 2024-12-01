from collections.abc import MutableSequence
import tkinter as tk
from time import sleep

class TkPixelStrip(MutableSequence):
    def __init__(self, num_pixels, brightness):
        self.num_pixels = num_pixels
        self.brightness = brightness
        self.list = [(0, 0, 0)]*num_pixels
        
        self.root = tk.Tk(screenName='LED strip')
        self.width = self.root.winfo_screenwidth()
        self.height = 20
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, -10, 0))
        self.canvas = tk.Canvas(master = self.root, 
                                width = self.width, 
                                height = self.height)
        self.canvas.configure(background='black')
        self.canvas.pack()
        
        self.pixelradius = self.width / (2 * (self.num_pixels + 1))
        self.draw()
        
        return
    
    def check(self, v):
        if not isinstance(v, tuple):
            raise TypeError("Value must be a tuple")
    
    def __getitem__(self, i): 
        return self.list[i]
    
    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v
        self.canvas.itemconfig(i + 1, fill = ('#%02x%02x%02x' % v))
        self.canvas.update()                                          
    
    def __delitem__(self, i):
        raise RuntimeError("Deletion not allowed")
    
    def __len__(self): 
        return len(self.list)
    
    def insert(self):
        raise RuntimeError("Insertion not allowed")
    
    def draw(self):
        # create led strip from current data
        y0 = (self.height / 2) - self.pixelradius
        y1 = (self.height / 2) + self.pixelradius
        
        for i in range(self.num_pixels):
            x0 = 2 * i * self.pixelradius
            x1 = 2 * (i + 1) * self.pixelradius
            self.canvas.create_oval(x0, y0, x1, y1, 
                                    width = 1,
                                    fill = ('#%02x%02x%02x' % self.list[i]),
                                    outline = 'gray')
        
        self.canvas.update()
    
    def show(self):
        pass
    
    def fill(self, v):
        self.check(v)
        self.list = [v]*self.num_pixels
        self.draw()
    
    def stop(self):
        self.root.destroy()
    
