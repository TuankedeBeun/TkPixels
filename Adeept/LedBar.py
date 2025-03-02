import RPi.GPIO as GPIO
import time

CMD_MODE = 0x0000 # Work on 8-bit mode
LED_ON = 0x00ff # 8-byte 1 data
LED_OFF = 0x0000 # 8-byte 0 data

def setup(data_pin, clk_pin):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(data_pin, GPIO.OUT)
	GPIO.setup(clk_pin,  GPIO.OUT)

	GPIO.output(data_pin, GPIO.LOW)
	GPIO.output(clk_pin,  GPIO.LOW)

def send_16bit_data(data, data_pin, clk_pin):
	clk_state = GPIO.HIGH
	
	for i in range(0, 16):
		# send one bit
		if data & 0x8000:
			data_state = GPIO.HIGH
		else:
			data_state = GPIO.LOW
		
		GPIO.output(data_pin, data_state)
		
		# tick the clock
		if clk_state == GPIO.HIGH:
			clk_state = GPIO.LOW
		else:
			clk_state = GPIO.HIGH
			
		GPIO.output(clk_pin, clk_state)
		
		time.sleep(0.0001)
		data <<= 1
  
def latch_data(data_pin):
	data_state = GPIO.LOW
	GPIO.output(data_pin, data_state)
	
	for i in range(8):
		if data_state == GPIO.LOW:
			data_state = GPIO.HIGH
		else:
			data_state = GPIO.LOW
		
		GPIO.output(data_pin, data_state)
  
def send_bar_data(bar_state, data_pin, clk_pin):
	for i in range(0, 12):
		if bar_state & 1:
			send_16bit_data(LED_ON, data_pin, clk_pin)
		else:
			send_16bit_data(LED_OFF, data_pin, clk_pin)
		bar_state >>= 1
		
def set_bar_state(bar_state, data_pin, clk_pin):
	send_16bit_data(CMD_MODE, data_pin, clk_pin)
	send_bar_data(bar_state, data_pin, clk_pin)
	latch_data(data_pin)

def set_single_led(led_nr, data_pin, clk_pin):
	bar_state = 2**(led_nr - 1)
	set_bar_state(bar_state, data_pin, clk_pin)

def set_cumulative_led(led_nr, data_pin, clk_pin):
	bar_state = 2**led_nr - 1
	set_bar_state(bar_state, data_pin, clk_pin)

def loop(data_pin, clk_pin):
	while True:
		led_state = 0x0000
		while led_state <= 0x03ff:
			#set_bar_state(led_state, data_pin, clk_pin)
			set_cumulative_led(4, data_pin, clk_pin)
			led_state = led_state*2+1
			time.sleep(0.05)

def blackout(data_pin, clk_pin):
	set_bar_state(0, data_pin, clk_pin)

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
	data_pin = 21
	clk_pin  = 20
	setup(data_pin, clk_pin)
	
	try:
		loop(data_pin, clk_pin)
	except KeyboardInterrupt:
		blackout(data_pin, clk_pin)
		destroy()
