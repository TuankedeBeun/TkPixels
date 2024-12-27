from TkPixels.Board import Board
from TkPixels.Controller import Controller

EFFECT_SET_NR = 4
BPM = 120
board = Board(1, EFFECT_SET_NR, simulate = True)
controller = Controller(board, BPM, EFFECT_SET_NR)
controller.play()