from collections import MutableSequence
import tkinter as tk
from time import sleep

class TkPixelStrip(MutableSequence):
    def __init__(self, num_pixels, brightness):
        self.num_pixels = num_pixels
        self.brightness = brightness
        self.list = [(0, 0, 0)]*num_pixels
        
        self.root = tk.Tk(screenName='LED strip')
        self.canvas = tk.Canvas(master=self.root, width=1200, height=200)
        self.canvas.pack()
        return
    
    def check(self, v):
        if not isinstance(v, tuple):
            raise TypeError("Value must be a tuple")
    
    def __getitem__(self, i): 
        return self.list[i]
    
    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v
    
    def __delitem__(self, i):
        raise RuntimeError("Deletion not allowed")
    
    def __len__(self): 
        return len(self.list)
    
    def insert(self):
        raise RuntimeError("Insertion not allowed")
    
    def draw(self):
        # create tkinter window with pixels
        pass
    
    def show(self):
        pass
    
    def fill(self, rgb):
        pass
    
    
    
    