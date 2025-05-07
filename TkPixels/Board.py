from os import path
import json
import tkinter as tk
from time import sleep
from math import sqrt
import numpy as np

class Board():
    def __init__(self, strip_right, strip_left, simulate = False, canvas = None, scale = 1):
        self.simulate = simulate
        self.strips = [strip_right, strip_left]
        self.scale = scale
        
        # load pixel data
        script_dir = path.dirname(path.abspath(__file__))
        file_path = path.join(script_dir, '../data/led_coordinates.json')
        self.pixeldata = load_pixel_data(file_path)
        self.num_pixels = len(self.pixeldata['indices'])
        self.num_pixels_per_strip = int(self.num_pixels / 2)

        # Draw tkinter LED strips when simulating
        if self.simulate:
            self.canvas = canvas
            self.draw()
    
    def draw(self, pixel_radius = 8):
        coords = self.pixeldata['coords_board']

        for (x, y) in coords:
            x0 = (x - pixel_radius) * self.scale
            x1 = (x + pixel_radius) * self.scale
            y0 = (y - pixel_radius) * self.scale
            y1 = (y + pixel_radius) * self.scale
            self.canvas.create_oval(
                x0, y0, x1, y1, 
                width = 1,
                fill = ('#%02x%02x%02x' % (0, 0, 0)),
                outline = '#363636'
            )
        
        self.canvas.update()

    def update(self):
        if self.simulate:
            self.canvas.update()
        else:
            self.strips[0].show()
            sleep(0.007)
            self.strips[1].show()
            
    def set_brightness(self, value):
        brightness = int(value * 128)
        for strip in self.strips:
            strip.set_brightness(brightness)
    
def load_pixel_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['indices'] = np.array(data['indices'])
    data['section_ids'] = np.array(data['section_ids'])
    data['coords_cart'] = np.array(data['coords_cart'])
    data['coords_spherical'] = np.array(data['coords_spherical'])

    return data
