import RPi.GPIO as GPIO
import time

BUTTON_PIN = 18
MEASUREMENTS = []

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set BtnPin's mode is input, and pull up to high level(3.3V)

def measurement(ev=None):
	global MEASUREMENTS
	now = time.time()
	
	if len(MEASUREMENTS) == 0:
		print('starting measurement...')
		MEASUREMENTS.append(now)
		
	elif now - MEASUREMENTS[-1] < 2:
		MEASUREMENTS.append(now)

def activate_button():
	GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=measurement, bouncetime=200) # wait for falling

def check_time():
	now = time.time()
	if len(MEASUREMENTS) == 0:
		return False
	else:
		return (now - MEASUREMENTS[-1] > 2)

def compute_bpm():
	global MEASUREMENTS
	
	if len(MEASUREMENTS) < 4:
		MEASUREMENTS = []
		print('Too few button presses to determine BPM...')
		return
		
	print('Determining BPM...')
	
	intervals = []
	for i in range(len(MEASUREMENTS) - 2):
		interval = MEASUREMENTS[i + 1] - MEASUREMENTS[i]
		intervals.append(interval)
		
	avg_intervals = sum(intervals) / len(intervals)
	bpm = 60 / avg_intervals
	
	MEASUREMENTS = []
	return bpm
	
