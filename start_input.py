import RPi.GPIO as GPIO
import Adeept.ADC0832 as adc
import Adeept.Button as btn
import time

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
	adc.setup()
	btn.setup()
	try:
		btn.activate_button()
		while True:
			pass
		#adc.loop()
	except KeyboardInterrupt:
		destroy()
