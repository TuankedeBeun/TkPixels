import RPi.GPIO as GPIO
import time

ADC_CS  = 8
ADC_CLK = 11
ADC_DIO = 9

TIME_LAST_CHECK = time.time()

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(ADC_CS, GPIO.OUT)
	GPIO.setup(ADC_CLK, GPIO.OUT)
	GPIO.setup(ADC_DIO, GPIO.IN)

def get_result(channel = 0):
	
	GPIO.output(ADC_CS, 0) # Activate ADC by setting CS to LOW
	GPIO.setup(ADC_DIO, GPIO.OUT) # Change DATA to OUT
	
	command = (1 << 3) | (1 << 2) | (channel << 1)
	
	# Sending start bits
	for i in range(4):
		bit = (command >> (3 - i)) & 1
		GPIO.output(ADC_DIO, bit)
		GPIO.output(ADC_CLK, True)
		time.sleep(0.001)
		GPIO.output(ADC_CLK, False)
	
	GPIO.setup(ADC_DIO, GPIO.IN) # Change DATA to IN
	
	value = 0
	for i in range(8):
		GPIO.output(ADC_CLK, 1)
		time.sleep(0.0001)
		bit = GPIO.input(ADC_DIO)
		value = (value << 1) | bit
		GPIO.output(ADC_CLK, 0)
	
	GPIO.output(ADC_CS, 1)
	return value

def write_value(file_path, value):
	pass

def check_time(interval=3):
	global TIME_LAST_CHECK
	current_time = time.time()
	
	if current_time - TIME_LAST_CHECK > interval:
		TIME_LAST_CHECK = current_time
		return True
	else:
		return False
	

