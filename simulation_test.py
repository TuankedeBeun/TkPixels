from TkPixels.Board import Board
from TkPixels.Controller import Controller

board = Board(0.8, pixelradius = 8, simulate = True)
controller = Controller(board, 120)
controller.play()