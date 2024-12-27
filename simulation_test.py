from TkPixels.Board import Board
from TkPixels.Controller import Controller

EFFECT_SET_NR = 0
BPM = 174
board = Board(1, EFFECT_SET_NR, simulate = True)
controller = Controller(board, BPM, EFFECT_SET_NR)
controller.play()