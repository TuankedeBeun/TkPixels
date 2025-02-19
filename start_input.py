import RPi.GPIO as GPIO
import Adeept.ADC0832 as adc
from Adeept import Settings
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

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	Settings.setup_pins(BUTTON_PIN_WHITE, BUTTON_PIN_RED, ADC_PIN_CS, ADC_PIN_CLK, ADC_PIN_DIO)
	
	try:
		Settings.activate_buttons(BUTTON_PIN_WHITE, BUTTON_PIN_RED)
		
		while True:
			setting, value = Settings.get_setting()
			
			if value != -1:
				Settings.write_to_file(DATA_PATH, setting, value)
				print(f'Saved setting {setting} = {value}\n')
	
	except KeyboardInterrupt:
		GPIO.cleanup()
		print('\npins are free')
