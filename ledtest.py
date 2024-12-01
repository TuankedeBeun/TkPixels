from rpi_ws281x import *

LED_COUNT = 120
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 50
LED_INVERT = False
LED_CHANNEL = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

for x in range(0, LED_COUNT):
    strip.setPixelColor(x,h Color(255,0,0))

strip.show()
