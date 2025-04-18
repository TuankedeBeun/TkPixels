from TkPixels.Board import Board
from TkPixels.Controller import Controller
from TkPixels.TkStripSequence import Strip
import tkinter as tk

LED_COUNT = 120
WIDTH = 410
HEIGHT = 780
BRIGHTNESS = 1

# create tkinter window and canvas
root = tk.Tk(screenName='LED strip')
root.geometry('%dx%d+%d+%d' % (root.winfo_screenwidth(), root.winfo_screenwidth(), 0, 0))
root.configure(background='black')
canvas = tk.Canvas(
    master = root, 
    width = WIDTH, 
    height = HEIGHT,
    background = 'black',
    highlightthickness = 1,
    highlightbackground = 'gray'
)
canvas.pack()

# create two tkinter led strips
strip_right = Strip(LED_COUNT, BRIGHTNESS, canvas, 1)
strip_left = Strip(LED_COUNT, BRIGHTNESS, canvas, 1 + LED_COUNT)

# initialize board and controller
board = Board(strip_right, strip_left, simulate=True, canvas=canvas)
controller = Controller(board)
controller.play()