from TkPixels.Board import Board
from TkPixels.Controller import Controller

EFFECT_SET_NR = 1
BPM = 87
board = Board(1, simulate = True)
controller = Controller(board, BPM, EFFECT_SET_NR)
controller.play()