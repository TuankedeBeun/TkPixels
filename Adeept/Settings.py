import RPi.GPIO as GPIO
import Adeept.ADC0832 as adc
import os
import time

SETTING_PIN = None
MEASUREMENT_PIN = None
CS_PIN = None
CLK_PIN = None
DIO_PIN = None

DATA_PATH = './data/settings.csv'
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

SETTINGS = ['state', 'bpm', 'mode', 'brightness', 'effect_intensity', 'number_of_colors']
SETTING_NR = -1
SETTING_VALUE = 0
TIME_LAST_PRESS = 0
BPM_MEASUREMENTS = []

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
	global SETTING_NR, SETTING_VALUE
	
	SETTING_NR = (SETTING_NR + 1) % len(SETTINGS)
	
	GPIO.remove_event_detect(MEASUREMENT_PIN)
	match SETTING_NR:
		case 0:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=toggle_state, bouncetime=150)
			print('Toggle state. Press the red button.')
			
		case 1:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=bpm_measurement, bouncetime=150)
			print('Configure BPM. Use the red button to tap the tempo.')
			
		case 2:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=mode_select, bouncetime=150)
			print('Select mode. Use the red button to shift through modes')
			
		case 3:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=slider_select, bouncetime=150)
			print('Configure brightness. Use the slider and select the brightness by pressing the red button.')
			
		case 4:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=slider_select, bouncetime=150)
			print('Configure effect intensity. Use the slider and select the instensity by pressing the red button.')
			
		case 5:
			GPIO.add_event_detect(MEASUREMENT_PIN, GPIO.FALLING, callback=slider_select, bouncetime=150)
			print('Configure number of colors. Use the slider and select the number by pressing the red button.')
			
	# read current setting from file
	with open(DATA_PATH, 'r') as file:
		lines = file.readlines()
		line = lines[SETTING_NR]
		splitted = line.split(',')
		print(f'Current setting: {splitted[0]} = {splitted[1]}')
		SETTING_VALUE = splitted[1]

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

def get_setting_value():
	global TIME_LAST_PRESS, SETTING_VALUE
	
	match SETTING_NR:
		case 0:
			setting_change = check_time(0)
			if setting_change:
				SETTING_VALUE = SETTING_VALUE
		
		case 1:
			setting_change = check_time(2)
			if setting_change:
				SETTING_VALUE = compute_bpm()
		
		case 2:
			setting_change = check_time(2)
			if setting_change:
				SETTING_VALUE = SETTING_VALUE
		
		case 3:
			setting_change = check_time(0)
			if setting_change:
				SETTING_VALUE = adc.get_result(CS_PIN, CLK_PIN, DIO_PIN)
		
		case 4:
			setting_change = check_time(0)
			if setting_change:
				SETTING_VALUE = adc.get_result(CS_PIN, CLK_PIN, DIO_PIN)
		
		case 5:
			setting_change = check_time(0)
			if setting_change:
				raw = adc.get_result(CS_PIN, CLK_PIN, DIO_PIN)
				SETTING_VALUE = int(raw * 5) + 1
	
	if setting_change:
		TIME_LAST_PRESS = 0
		return SETTING_VALUE
	else:
		return -1

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

def toggle_state(ev=None):
	global SETTING_VALUE, TIME_LAST_PRESS
	SETTING_VALUE = int(not SETTING_VALUE)
	TIME_LAST_PRESS = time.time()

def mode_select(ev=None):
	global SETTING_VALUE, TIME_LAST_PRESS
	SETTING_VALUE = (SETTING_VALUE + 1) % 10
	TIME_LAST_PRESS = time.time()
	
def slider_select(ev=None):
	global TIME_LAST_PRESS
	TIME_LAST_PRESS = time.time()

def write_to_file(value, setting_nr=None):
	### Write a specific setting to the settings file
	
	if setting_nr == None:
		setting_nr = SETTING_NR
	
	# validate setting name
	if setting_nr > len(SETTINGS):
		raise ValueError('Setting number %d is not valid' % setting_nr)
	
	# Read current settings
	lines = []
	with open(DATA_PATH, 'r') as file:
		lines = file.readlines()
	
	# Change one setting
	line_number = setting_nr
	setting_name = SETTINGS[setting_nr]
	lines[line_number] = f'{setting_name},{value}\n'
	
	# Write modified settings
	with open(DATA_PATH, 'w') as file:
		file.writelines(lines)
	
	print(f'Saved setting: {setting_name} = {value}\n')
