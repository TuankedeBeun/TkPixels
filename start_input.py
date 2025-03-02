import RPi.GPIO as GPIO
import Adeept.ADC0832 as adc
from Adeept import Settings, LedBar
import time

# GPIO pins
BUTTON_PIN_RED = 5
BUTTON_PIN_WHITE = 6
ADC_PIN_CS = 8
ADC_PIN_CLK = 11
ADC_PIN_DIO = 9
LEDBAR_PIN_DATA = 21
LEDBAR_PIN_CLK = 20

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	Settings.setup_pins(BUTTON_PIN_WHITE, BUTTON_PIN_RED, ADC_PIN_CS, ADC_PIN_CLK, ADC_PIN_DIO)
	LedBar.setup_pins(LEDBAR_PIN_DATA, LEDBAR_PIN_CLK)
	
	try:
		Settings.activate_buttons(BUTTON_PIN_WHITE, BUTTON_PIN_RED)
		
		while True:
			value = Settings.get_setting_value()
			
			if value != -1:
				Settings.write_to_file(value)
				LedBar.setting_changed()
				
			LedBar.determine_output(Settings.SETTING_NR, Settings.SETTING_VALUE)
	
	except KeyboardInterrupt:
		print('')
		Settings.write_to_file(0, setting_nr=0) # always turn off state
		GPIO.cleanup()
		print('pins are free')
