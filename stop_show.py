import RPi.GPIO as GPIO
import os
import signal

BUTTON_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def shutdown_or_stop(channel):
    # Kill the LED script process
    os.system("pkill -f /home/tuanke/Programming/TkPixels/led_show.py")

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=shutdown_or_stop, bouncetime=200)

try:
    print("Press the button to stop the LED scrip.")
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()