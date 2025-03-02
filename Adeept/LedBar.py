import RPi.GPIO as GPIO
import time

DATA_PIN = None
CLK_PIN = None

CMD_MODE = 0x0000 # Work on 8-bit mode
LED_ON = 0x00ff # 8-byte 1 data
LED_OFF = 0x0000 # 8-byte 0 data

BLINK_STATE = False
TIME_LAST_CHANGED = 0
SWIPE_STATE = 0
TIME_STATE_CHANGED = 0

def setup_pins(data_pin, clk_pin):
	global DATA_PIN, CLK_PIN
	DATA_PIN = data_pin
	CLK_PIN = clk_pin
	
	GPIO.setup(data_pin, GPIO.OUT)
	GPIO.setup(clk_pin,  GPIO.OUT)

	GPIO.output(data_pin, GPIO.LOW)
	GPIO.output(clk_pin,  GPIO.LOW)
	
def reset_state():
	global BLINK_STATE, TIME_LAST_CHANGED, SWIPE_STATE
	BLINK_STATE = False
	TIME_LAST_CHANGED = 0
	SWIPE_STATE = 0
	TIME_STATE_CHANGED = 0
	
def setting_changed():
	global TIME_STATE_CHANGED
	TIME_STATE_CHANGED = time.time()

def send_16bit_data(data):
	clk_state = GPIO.HIGH
	
	for i in range(0, 16):
		# send one bit
		if data & 0x8000:
			data_state = GPIO.HIGH
		else:
			data_state = GPIO.LOW
		
		GPIO.output(DATA_PIN, data_state)
		
		# tick the clock
		if clk_state == GPIO.HIGH:
			clk_state = GPIO.LOW
		else:
			clk_state = GPIO.HIGH
			
		GPIO.output(CLK_PIN, clk_state)
		
		time.sleep(0.0001)
		data <<= 1
  
def latch_data():
	data_state = GPIO.LOW
	GPIO.output(DATA_PIN, data_state)
	
	for i in range(8):
		if data_state == GPIO.LOW:
			data_state = GPIO.HIGH
		else:
			data_state = GPIO.LOW
		
		GPIO.output(DATA_PIN, data_state)
  
def send_bar_data(bar_state):
	for i in range(0, 12):
		if bar_state & 1:
			send_16bit_data(LED_ON)
		else:
			send_16bit_data(LED_OFF)
		bar_state >>= 1
		
def set_bar_state(bar_state):
	send_16bit_data(CMD_MODE)
	send_bar_data(bar_state)
	latch_data()

def set_single_led(led_nr):
	bar_state = 2**(led_nr - 1)
	set_bar_state(bar_state)

def set_cumulative_leds(led_nr):
	bar_state = 2**led_nr - 1
	set_bar_state(bar_state)

# used for selecting kind of setting
def blink_cumulative_leds(led_nr, frequency=2):
	global TIME_LAST_CHANGED, BLINK_STATE
	
	wait_time = 1 / (2 * frequency)
	now = time.time()
	
	if now - TIME_LAST_CHANGED < wait_time:
		return
	
	if BLINK_STATE == 0:
		set_cumulative_leds(led_nr)
	else:
		blackout()
	
	BLINK_STATE = not BLINK_STATE
	TIME_LAST_CHANGED = now
	
# used when setting state to ON
def swipe_full(frequency=10, reverse=False):
	global TIME_LAST_CHANGED, SWIPE_STATE
	
	wait_time = 1 / frequency
	now = time.time()
	
	if now - TIME_LAST_CHANGED < wait_time:
		return
	
	if reverse:
		SWIPE_STATE = max(0, SWIPE_STATE - 1)
	else:
		SWIPE_STATE = min(10, SWIPE_STATE + 1)
	
	set_cumulative_leds(SWIPE_STATE)
	TIME_LAST_CHANGED = now

def determine_output(setting_nr, setting_value):
	global TIME_STATE_CHANGED
	
	now = time.time()
	
	if now - TIME_STATE_CHANGED > 2:
		blink_cumulative_leds(setting_nr + 1)
		return
	
	match setting_nr:
		case 0:
			reverse = not setting_value
			swipe_full(reverse=reverse)
		
		case 1:
			bpm_min = 60
			bpm_max = 200
			bpm_diff = bpm_max - bpm_min
			fraction = (setting_value - bpm_min) / bpm_diff
			tens = int(round(10 * fraction, 0))
			tens = max(0, min(10, tens)) # stay within bounds [0, 10]
			set_cumulative_leds(tens)
		
		case 2:
			set_cumulative_leds(setting_value + 1)
		
		case 3:
			set_cumulative_leds(int(round(10 * setting_value, 0)))
		
		case 4:
			set_cumulative_leds(int(round(10 * setting_value, 0)))
		
		case 5:
			set_cumulative_leds(setting_value)
	
def blackout():
	set_bar_state(0)

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
	data_pin = 21
	clk_pin  = 20
	setup(data_pin, clk_pin)
	
	try:
		determine_output(0, 1)
	except KeyboardInterrupt:
		blackout()
		destroy()
