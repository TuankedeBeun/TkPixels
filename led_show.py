from TkPixels.Board import Board
from TkPixels.Controller import Controller

board = Board(0.8, simulate=False)
controller = Controller(board, 174)
controller.play()