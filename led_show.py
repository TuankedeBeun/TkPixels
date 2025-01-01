from TkPixels.Board import Board
from TkPixels.Controller import Controller

BPM = 174
BRIGHTNESS = 0.6

board = Board(brightness=BRIGHTNESS)
controller = Controller(board, BPM)
controller.play()
