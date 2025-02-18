import RPi.GPIO as GPIO
import Adeept.ADC0832 as adc
import Adeept.Button as btn
import time
import os

DATA_PATH = './data/settings.csv'
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

def write_to_file(setting, value):
	
	settings = {'brightness':0, 'bpm':1}
	if setting not in settings.keys():
		raise ValueError('Setting %s is not valid' % setting)
	
	lines = []
	try:
		with open(DATA_PATH, 'r') as file:
			lines = file.readlines()
	except FileNotFoundError:
		pass
		
	line_number = settings[setting]
	value = round(value, 2)
	lines[line_number] = f'{setting},{value}\n'
	
	with open(DATA_PATH, 'w') as file:
		file.writelines(lines)

def destroy():
	GPIO.cleanup()
	print('\npins freed')

if __name__ == '__main__':
	adc.setup()
	btn.setup()
	try:
		btn.activate_button()
		while True:
			if (adc.check_time()):
				brightness = adc.get_result()
				write_to_file('brightness', brightness)
				print('slider', brightness)
				
			if (btn.check_time()):
				bpm = btn.compute_bpm()
				if bpm:
					write_to_file('bpm', bpm)
					print('bpm', bpm)
	
	except KeyboardInterrupt:
		destroy()
