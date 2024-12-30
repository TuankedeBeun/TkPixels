from TkPixels.Board import Board
from TkPixels.Controller import Controller

EFFECT_SET_NR = 2
BPM = 120

board = Board(simulate = True)
controller = Controller(board, BPM, EFFECT_SET_NR)
controller.play()