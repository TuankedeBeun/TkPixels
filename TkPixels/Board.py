# import .\StripDesign
import json
import tkinter as tk
from time import sleep
from math import sqrt

class Board():
    def __init__(self, brightness, pixel_size = 10, width = 500, height = 750):
        self.brightness = brightness
        self.width = width
        self.height = height
        self.pixelradius = pixel_size
        
        # initialize window
        self.root = tk.Tk(screenName='LED strip')
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, 50, 50))
        self.canvas = tk.Canvas(master = self.root, 
                                width = self.width, 
                                height = self.height)
        self.canvas.configure(background='black')
        self.canvas.pack()
        
        # draw pixels
        self.pixeldata = load_pixel_data('data/led_coordinates.json')
        self.num_pixels_per_strip = int(len(self.pixeldata['indices']) / 2)
        self.draw()
        
        return
    
    def draw(self):
        coords = self.pixeldata['coords_board']

        for (x, y) in coords:
            x0 = x - self.pixelradius
            x1 = x + self.pixelradius
            y0 = y - self.pixelradius
            y1 = y + self.pixelradius
            self.canvas.create_oval(
                x0, y0, x1, y1, 
                width = 1,
                fill = ('#%02x%02x%02x' % (0, 0, 0)),
                outline = 'gray'
            )
        
        self.canvas.update()
    
    def stop(self):
        self.root.destroy()
    
def load_pixel_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data