from TkPixels.Board import Board
from TkPixels.Controller import Controller
from rpi_ws281x import ws, Color, PixelStrip

BPM = 150
BRIGHTNESS = 0.6

LED_COUNT = 120
LED_FREQ_HZ = 800000
LED_BRIGHTNESS = 128
LED_INVERT = False
LED_STRIP = ws.WS2811_STRIP_RGB

LED_1_PIN = 18
LED_1_DMA = 10
LED_1_CHANNEL = 0

LED_2_PIN = 13
LED_2_DMA = 14
LED_2_CHANNEL = 1

# create two LED strip instances
strip_right = PixelStrip(LED_COUNT, LED_1_PIN, LED_FREQ_HZ,
                    LED_1_DMA, LED_INVERT, LED_BRIGHTNESS,
                    LED_1_CHANNEL, LED_STRIP)

strip_left = PixelStrip(LED_COUNT, LED_2_PIN, LED_FREQ_HZ,
                    LED_2_DMA, LED_INVERT, LED_BRIGHTNESS,
                    LED_2_CHANNEL, LED_STRIP)

# initialize library
strip_right.begin()
strip_left.begin()

board = Board(strip_right, strip_left)
controller = Controller(board, BPM)
controller.play()
