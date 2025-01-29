from time import sleep
from TkPixels.Board import Board
from TkPixels.Controller import Controller
from TkPixels.PixelStripSequence import Strip

BPM = 140
BRIGHTNESS = 128

LED_1_PIN = 18
LED_1_DMA = 10
LED_1_CHANNEL = 0

LED_2_PIN = 13
LED_2_DMA = 14
LED_2_CHANNEL = 1

# create two LED strip instances
strip_right = Strip(LED_1_PIN, LED_1_DMA, LED_1_CHANNEL, BRIGHTNESS)
strip_left = Strip(LED_2_PIN, LED_2_DMA, LED_2_CHANNEL, BRIGHTNESS)

board = Board(strip_right, strip_left)
controller = Controller(board, BPM)

try:
	controller.play()
except KeyboardInterrupt:
	strip_right.fill((0,0,0))
	strip_right.show()
	sleep(0.01)
	strip_left.fill((0,0,0))
	strip_left.show()
	sleep(0.01)
