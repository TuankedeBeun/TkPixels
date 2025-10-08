import RPi.GPIO as GPIO
import time

def setup(cs, clk, dio):
	GPIO.setup(cs, GPIO.OUT)
	GPIO.setup(clk, GPIO.OUT)
	GPIO.setup(dio, GPIO.IN)

def get_result(cs, clk, dio, channel = 0):
	
	# Activate ADC
	GPIO.output(cs, 0)
	
	# Sending start bits
	GPIO.setup(dio, GPIO.OUT)
	command = (1 << 3) | (1 << 2) | (channel << 1)
	
	for i in range(4):
		bit = (command >> (3 - i)) & 1
		GPIO.output(dio, bit)
		GPIO.output(clk, True)
		time.sleep(0.001)
		GPIO.output(clk, False)
	
	
	# Read byte
	GPIO.setup(dio, GPIO.IN)
	value = 0
	
	for i in range(8):
		GPIO.output(clk, 1)
		time.sleep(0.0001)
		bit = GPIO.input(dio)
		value = (value << 1) | bit
		GPIO.output(clk, 0)
	
	# Deactivate ADC
	GPIO.output(cs, 1)
	
	# Normalize value
	value = round(value / 255, 2)
	
	return value
