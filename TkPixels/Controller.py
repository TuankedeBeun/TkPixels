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
                self.board.strips[0].fill((0, 0, 0))
                self.board.strips[1].fill((0, 0, 0))
                self.update_canvas()
                on = False
            else:
                hue = random()
                rgb = hsv_to_rgb(hue, 1, 1)
                rgb = tuple([int(255 * i) for i in rgb])
                self.board.strips[0].fill(rgb)
                self.board.strips[1].fill(rgb)
                self.update_canvas()
                on = True

            sleep(0.1)

    def update_canvas(self):
        self.board.canvas.update()
