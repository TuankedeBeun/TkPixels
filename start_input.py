import RPi.GPIO as GPIO
import Adeept.ADC0832 as adc
import Adeept.Button as btn
import time
import os

DATA_PATH = './data/settings.csv'
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

# GPIO pins
BUTTON_PIN_RED = 5
BUTTON_PIN_WHITE = 6
ADC_PIN_CS = 8
ADC_PIN_CLK = 11
ADC_PIN_DIO = 9


def write_to_file(setting, value):
	### Write a specific setting to the settings file
	
	# validate setting name
	settings = {'brightness':0, 'bpm':1, 'mode':2}
	if setting not in settings.keys():
		raise ValueError('Setting %s is not valid' % setting)
	
	# Read current settings
	lines = []
	try:
		with open(DATA_PATH, 'r') as file:
			lines = file.readlines()
	except FileNotFoundError:
		pass
	
	# Change one setting
	line_number = settings[setting]
	value = round(value, 2)
	lines[line_number] = f'{setting},{value}\n'
	
	# Write modified settings
	with open(DATA_PATH, 'w') as file:
		file.writelines(lines)

def destroy():
	GPIO.cleanup()
	print('\npins freed')

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	adc.setup(ADC_PIN_CS, ADC_PIN_CLK, ADC_PIN_DIO)
	btn.setup(BUTTON_PIN_RED)
	btn.setup(BUTTON_PIN_WHITE)
	
	try:
		btn.activate_buttons(BUTTON_PIN_WHITE, BUTTON_PIN_RED)
		
		while True:
			if (adc.check_time(interval=10)):
				brightness = adc.get_result(ADC_PIN_CS, ADC_PIN_CLK, ADC_PIN_DIO)
				write_to_file('brightness', brightness)
				print('slider', brightness)
				
			if (btn.check_time()):
				setting, value = btn.get_setting()
				if value != -1:
					write_to_file(setting, value)
					print(f'Saved setting {setting} = {value}')
	
	except KeyboardInterrupt:
		destroy()
