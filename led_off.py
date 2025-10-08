from rpi_ws281x import *

LED_COUNT = 240
LED_FREQ_HZ = 800000
LED_BRIGHTNESS = 50
LED_INVERT = False
LED_CHANNEL = 0

# Only the GPIO Pin number and the DMA channel must differ
strip1 = Adafruit_NeoPixel(LED_COUNT, 18, LED_FREQ_HZ, 9, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip1.begin()
strip1.show()
del strip1

strip1 = Adafruit_NeoPixel(LED_COUNT, 21, LED_FREQ_HZ, 10, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip1.begin()
strip1.show()
del strip1
