import RPi.GPIO as GPIO
import time

SETTING = -1
MEASUREMENT_PIN = None
TIME_LAST_PRESS = 0
BPM_MEASUREMENTS = []
MODE = 0

def setup(pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set BtnPin's mode is input, and pull up to high level(3.3V)
	
def shift_setting(ev=None):
	global SETTING
	
	SETTING = (SETTING + 1) % 2
	
	GPIO.remove_event_detect(MEASUREMENT_PIN)
	match SETTING:
		case 0:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=bpm_measurement, bouncetime=150)
			print('Waiting for BPM measurements')
			
		case 1:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=mode_select, bouncetime=150)
			print('Mode select')

def activate_buttons(settings_pin, measurement_pin):
	global MEASUREMENT_PIN
	MEASUREMENT_PIN = measurement_pin
	shift_setting()
	GPIO.add_event_detect(settings_pin, GPIO.FALLING, callback=shift_setting, bouncetime=200)

def check_time(wait_time_seconds=2):
	now = time.time()
	if TIME_LAST_PRESS == 0:
		return False
	else:
		return (now - TIME_LAST_PRESS > wait_time_seconds)

def get_setting():
	global TIME_LAST_PRESS
	match SETTING:
		case 0:
			value = compute_bpm()
			setting = 'bpm'
		case 1:
			value = MODE
			setting = 'mode'
	
	TIME_LAST_PRESS = 0
	
	return setting, value

def bpm_measurement(ev=None):
	global BPM_MEASUREMENTS, TIME_LAST_PRESS
	now = time.time()
	
	if len(BPM_MEASUREMENTS) == 0:
		print('starting measurement...')
	
	BPM_MEASUREMENTS.append(now)
	TIME_LAST_PRESS = time.time()

def compute_bpm():
	global BPM_MEASUREMENTS
	
	print('Got %d button presses' % len(BPM_MEASUREMENTS))
	
	if len(BPM_MEASUREMENTS) < 4:
		BPM_MEASUREMENTS = []
		print('Too few button presses to determine BPM...')
		return -1
		
	print('Determining BPM...')
	
	time_total = BPM_MEASUREMENTS[-1] - BPM_MEASUREMENTS[0]
	n_intervals = len(BPM_MEASUREMENTS) - 1
	time_avg = time_total / n_intervals
	bpm = round(60 / time_avg, 1)
	
	BPM_MEASUREMENTS = []
	return bpm

def mode_select(ev=None):
	global MODE, TIME_LAST_PRESS
	MODE = MODE + 1) % 10
	TIME_LAST_PRESS = time.time()
