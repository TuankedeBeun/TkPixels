from TkPixels.Board import Board
from TkPixels.Controller import Controller

board = Board(1, pixelradius = 8, simulate = True)
controller = Controller(board, 120)
controller.play()