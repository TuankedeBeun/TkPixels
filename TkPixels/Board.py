from os import path
from TkPixels.StripDesign import Strip
# import board
# import neopixel
import json
import tkinter as tk
from time import time, sleep
from math import sqrt
import numpy as np

class Board():
    def __init__(self, brightness, effect_set_nr, pixelradius = 8, width = 500, height = 750, simulate = True):
        self.brightness = brightness
        self.effect_set_nr = effect_set_nr
        self.width = width
        self.height = height
        self.pixelradius = pixelradius
        self.simulate = simulate
        self.getting_effect = False
        
        # load pixel data
        script_dir = path.dirname(path.abspath(__file__))
        file_path = path.join(script_dir, '..\\data\\led_coordinates.json')
        self.pixeldata = load_pixel_data(file_path)
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

            # button to set effect + two leds
            self.effect_slider = tk.Scale(
                self.canvas, from_=100, to=0, bg='#222222', borderwidth=0, fg='white', 
                highlightthickness=0, troughcolor='black'
            )
            self.effect_slider.place(x=self.width/2, y=self.height, anchor=tk.S)
            self.led_red = self.canvas.create_oval(self.width/2 - 100, self.height - 20, self.width/2 - 80, self.height, fill='black', outline='#333333', width=2)
            self.led_green = self.canvas.create_oval(self.width/2 + 100, self.height - 20, self.width/2 + 80, self.height, fill='black', outline='#333333', width=2)

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

    def get_effect_nr(self):
        val = int(self.effect_slider.get())

        if self.getting_effect:
            if val < 10:
                self.effect_set_nr = 0

            elif val < 20:
                self.effect_set_nr = 1

            elif val < 30:
                self.effect_set_nr = 2

            elif val < 40:
                self.effect_set_nr = 3

            elif val < 50:
                self.effect_set_nr = 4

            elif val < 60:
                self.effect_set_nr = 5
            
            else:
                # value is too high
                self.canvas.itemconfig(self.led_red, fill='black')
                self.canvas.update()
                self.effect_start_time = 0
                self.getting_effect = False
                return self.effect_set_nr

            print('effect set number', self.effect_set_nr)
            self.canvas.itemconfig(self.led_red, fill='black')
            self.canvas.itemconfig(self.led_green, fill='green')
            self.effect_start_time = 0
            self.getting_effect = False

        elif not self.getting_effect:
            if val < 10:
                self.canvas.itemconfig(self.led_red, fill='red')
                self.canvas.itemconfig(self.led_green, fill='black')
                self.getting_effect = True
            else:
                self.canvas.itemconfig(self.led_red, fill='black')
                self.canvas.itemconfig(self.led_green, fill='black')
                self.getting_effect = False

        return self.effect_set_nr

    def set_effect_nr(self, val):
        if self.effect_start_time == 0 or time() - self.effect_start_time < 1:
            self.effect_start_time = time()
            self.canvas.itemconfig(self.led_red, fill='red')

        elif time() - self.effect_start_time > 5:
            self.canvas.itemconfig(self.led_red, fill='black')
            self.effect_start_time = 0

        else:
            val = int(self.effect_slider.get())
            if val < 10:
                self.effect_set_nr = 0

            elif val < 20:
                self.effect_set_nr = 1

            elif val < 30:
                self.effect_set_nr = 2

            elif val < 40:
                self.effect_set_nr = 3

            elif val < 50:
                self.effect_set_nr = 5
            
            else:
                # value is too high
                self.canvas.itemconfig(self.led_red, fill='black')
                self.canvas.update()
                self.effect_start_time = 0
                return

            print('effect set number', self.effect_set_nr)
            self.canvas.itemconfig(self.led_red, fill='black')
            self.canvas.itemconfig(self.led_green, fill='green')
            self.effect_start_time = 0

        
        
    
def load_pixel_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data['indices'] = np.array(data['indices'])
    data['section_ids'] = np.array(data['section_ids'])
    data['coords_cart'] = np.array(data['coords_cart'])
    data['coords_spherical'] = np.array(data['coords_spherical'])

    return data
    