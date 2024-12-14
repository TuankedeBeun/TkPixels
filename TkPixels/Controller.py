from time import sleep
from colorsys import hsv_to_rgb
from random import random

class Controller():
    def __init__(self, board, bpm):
        self.board = board
        self.bpm = bpm
        self.time = 0
        self.phrase = 0
        self.bar = 0
        self.beat = 0

    def play(self):
        on = False
        while True:
            if on:
                vectors = [(0,0,0)] * self.board.num_pixels
                on = False
            else:
                hue = random()
                rgb = hsv_to_rgb(hue, 1, 1)
                rgb = tuple([int(255 * i) for i in rgb])
                vectors = [rgb] * self.board.num_pixels
                on = True

            self.draw_strips(vectors)
            sleep(0.1)

    def draw_strips(self, vectors):
        for (strip, led), v in zip(self.board.pixeldata['indices'], vectors):
            self.board.strips[strip][led] = v
        
        self.update_canvas()

    def effect_pixel_height(self, hue, height):
        return 

    def update_canvas(self):
        self.board.canvas.update()
