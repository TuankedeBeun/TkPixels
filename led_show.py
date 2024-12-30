from TkPixels.Board import Board
from TkPixels.Controller import Controller

EFFECT_SET_NR = 0
BPM = 120

board = Board()
controller = Controller(board, BPM, EFFECT_SET_NR)
controller.play()