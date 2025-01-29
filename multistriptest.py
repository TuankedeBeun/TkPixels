from time import sleep
from rpi_ws281x import ws, Color, PixelStrip

LED_1_COUNT = 120
LED_1_PIN = 18
LED_1_FREQ_HZ = 800000
LED_1_DMA = 10
LED_1_BRIGHTNESS = 128
LED_1_INVERT = False
LED_1_CHANNEL = 0
LED_1_STRIP = ws.WS2811_STRIP_RGB

LED_2_COUNT = 120
LED_2_PIN = 13
LED_2_FREQ_HZ = 800000
LED_2_DMA = 14
LED_2_BRIGHTNESS = 128
LED_2_INVERT = False
LED_2_CHANNEL = 1
LED_2_STRIP = ws.WS2811_STRIP_RGB


def snake(strip, color, pixel):
    
    for i in range(strip.numPixels()):
        if i == pixel:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, 0)


def blackout(strip):
    
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))


if __name__ == '__main__':
    strip1 = PixelStrip(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ,
                               LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS,
                               LED_1_CHANNEL, LED_1_STRIP)
    
    strip2 = PixelStrip(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ,
                               LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS,
                               LED_2_CHANNEL, LED_2_STRIP)

    # Initialize library
    strip1.begin()
    strip2.begin()
    
    print('Press CTRL-C to quit')
    
    # Black out any LEDs that are still on from last run
    blackout(strip1)
    strip1.show()
    sleep(0.01)
    blackout(strip2)
    strip2.show()
    sleep(0.01)
    
    try:
        while True:
            for t in range(120):
                snake(strip1, Color(255, 0, 0), t)
                snake(strip2, Color(0, 255, 0), t)
                strip1.show()
                sleep(0.005) # must be minamlly 5 ms
                strip2.show()
                sleep(0.005) # necessary after each show
        
    except KeyboardInterrupt:
        blackout(strip1)
        strip1.show()
        sleep(0.01)
        blackout(strip2)
        strip2.show()
        sleep(0.01)
