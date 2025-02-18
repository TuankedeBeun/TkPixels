import RPi.GPIO as GPIO

BUTTON_PIN = 18
STATUS = 0

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set BtnPin's mode is input, and pull up to high level(3.3V)

def swLed(ev=None):
	global STATUS
	STATUS = not STATUS
	if STATUS == 1:
		print('led off...')
	else:
		print('...led on')

def activate_button():
	GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=swLed, bouncetime=200) # wait for falling
