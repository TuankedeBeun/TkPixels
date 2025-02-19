import RPi.GPIO as GPIO
import Adeept.ADC0832 as adc
import time

SETTING_PIN = None
MEASUREMENT_PIN = None
CS_PIN = None
CLK_PIN = None
DIO_PIN = None

NUMBER_OF_SETTINGS = 4
SETTING = -1
TIME_LAST_PRESS = 0
BPM_MEASUREMENTS = []
MODE = 0

def setup_pins(setting, measurement, cs, clk, dio):
	global SETTING_PIN, MEASUREMENT_PIN, CS_PIN, CLK_PIN, DIO_PIN
	
	# configure GPIO's
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(setting, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(measurement, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	adc.setup(cs, clk, dio)
	
	# copy pins as globals
	SETTING_PIN = setting
	MEASUREMENT_PIN = measurement
	CS_PIN = cs
	CLK_PIN = clk
	DIO_PIN = dio
	
def shift_setting(ev=None):
	global SETTING
	
	SETTING = (SETTING + 1) % NUMBER_OF_SETTINGS
	
	GPIO.remove_event_detect(MEASUREMENT_PIN)
	match SETTING:
		case 0:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=bpm_measurement, bouncetime=150)
			print('Configure BPM. Use the red button to tap the tempo.')
			
		case 1:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=mode_select, bouncetime=150)
			print('Select mode. Use the red button to shift through modes')
			
		case 2:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=slider_select, bouncetime=150)
			print('Configure brightness. Use the slider and select the brightness by pressing th red button.')
			
		case 3:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=slider_select, bouncetime=150)
			print('Configure effect intensity. Use the slider and select the instensity by pressing th red button.')

def activate_buttons(settings_pin, measurement_pin):
	global MEASUREMENT_PIN
	MEASUREMENT_PIN = measurement_pin
	shift_setting()
	GPIO.add_event_detect(settings_pin, GPIO.FALLING, callback=shift_setting, bouncetime=200)

def check_time(wait_time_seconds):
	now = time.time()
	if TIME_LAST_PRESS == 0:
		return False
	else:
		return (now - TIME_LAST_PRESS > wait_time_seconds)

def get_setting():
	global TIME_LAST_PRESS
	
	value = -1
	
	match SETTING:
		case 0:
			setting = 'bpm'
			if (check_time(2)):
				value = compute_bpm()
			
		case 1:
			setting = 'mode'
			if (check_time(2)):
				value = MODE
			
		case 2:
			setting = 'brightness'
			if (check_time(0)):
				value = adc.get_result(CS_PIN, CLK_PIN, DIO_PIN)
			
		case 3:
			setting = 'effect_intensity'
			if (check_time(0)):
				value = adc.get_result(CS_PIN, CLK_PIN, DIO_PIN)
	
	if value != -1:
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
	MODE = (MODE + 1) % 10
	TIME_LAST_PRESS = time.time()
	
def slider_select(ev=None):
	global TIME_LAST_PRESS
	TIME_LAST_PRESS = time.time()
	
def write_to_file(file_path, setting, value):
	### Write a specific setting to the settings file
	
	# validate setting name
	settings = {'bpm':0, 'mode':1, 'brightness':2, 'effect_intensity':3}
	if setting not in settings.keys():
		raise ValueError('Setting %s is not valid' % setting)
	
	# Read current settings
	lines = []
	try:
		with open(file_path, 'r') as file:
			lines = file.readlines()
	except FileNotFoundError:
		pass
	
	# Change one setting
	line_number = settings[setting]
	lines[line_number] = f'{setting},{value}\n'
	
	# Write modified settings
	with open(file_path, 'w') as file:
		file.writelines(lines)
