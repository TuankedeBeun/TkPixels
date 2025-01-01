from TkPixels.Board import Board
from TkPixels.Controller import Controller

BPM = 143

board = Board()
controller = Controller(board, BPM)
controller.play()
