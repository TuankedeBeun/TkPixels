import RPi.GPIO as GPIO
import time

ADC_CS  = 8
ADC_CLK = 11
ADC_DIO = 9

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(ADC_CS, GPIO.OUT)
	GPIO.setup(ADC_CLK, GPIO.OUT)
	GPIO.setup(ADC_DIO, GPIO.IN)

def getResult(channel = 0):
	
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

def loop(interval=1):
	while True:
		t = getResult()
		write_value('data.txt', t)
		vol = 5.0/255 * t
		vol = round(vol, 2)
		print('Original', t, 'Voltage', vol)
		time.sleep(interval)

