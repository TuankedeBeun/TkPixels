from TkPixels.StripDesign import Strip
# import board
# import neopixel
import json
import tkinter as tk
from time import sleep
from math import sqrt
import numpy as np

class Board():
    def __init__(self, brightness, pixelradius = 10, width = 500, height = 750, simulate = True):
        self.brightness = brightness
        self.width = width
        self.height = height
        self.pixelradius = pixelradius
        self.simulate = simulate
        
        # load pixel data
        self.pixeldata = load_pixel_data('data/led_coordinates.json')
        self.num_pixels = len(self.pixeldata['indices'])
        self.num_pixels_per_strip = int(self.num_pixels / 2)

        # initialize window
        if self.simulate:
            self.root = tk.Tk(screenName='LED strip')
            self.root.geometry('%dx%d+%d+%d' % (self.root.winfo_screenwidth(), self.root.winfo_screenwidth(), 0, 0))
            self.root.configure(background='black')
            self.canvas = tk.Canvas(
                master = self.root, 
                width = self.width, 
                height = self.height,
                background = 'black',
                highlightthickness = 1,
                highlightbackground = 'gray'
            )
            self.canvas.pack()
            
            # draw pixels
            self.draw()

            # initialize two led strips
            strip_r = Strip(self.num_pixels_per_strip, self.brightness, self.canvas, 1)
            strip_l = Strip(self.num_pixels_per_strip, self.brightness, self.canvas, 1 + self.num_pixels_per_strip)
            self.strips = [strip_r, strip_l]

        else:
            strip_r = neopixel.NeoPixel(board.D18, self.num_pixels_per_strip, brightness=self.brightness, auto_write=False)
            strip_l = neopixel.NeoPixel(board.D21, self.num_pixels_per_strip, brightness=self.brightness, auto_write=False)

        self.strips = [strip_r, strip_l]
        
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

    def update(self):
        if self.simulate:
            self.canvas.update()
        else:
            self.strips[0].show()
            self.strips[1].show()
    
    def stop(self):
        self.root.destroy()
    
def load_pixel_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['indices'] = np.array(data['indices'])
    data['coords_cart'] = np.array(data['coords_cart'])

    return data