# TODO: Rewrite this LedBar and ADC in OOP.
import RPi.GPIO as GPIO
import time

DATA_PIN = None
CLK_PIN = None

CMD_MODE = 0x0000 # Work on 8-bit mode

TIME_LAST_CHANGED = 0
SWIPE_STATE = 0
BLINK_STATE = 0

def setup_pins(data_pin, clk_pin):
	global DATA_PIN, CLK_PIN
	DATA_PIN = data_pin
	CLK_PIN = clk_pin
	
	GPIO.setup(data_pin, GPIO.OUT)
	GPIO.setup(clk_pin,  GPIO.OUT)

	GPIO.output(data_pin, GPIO.LOW)
	GPIO.output(clk_pin,  GPIO.LOW)

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

# used for selecting kind of setting
def set_single_led(led):
	bar_state = 2**(led - 1)
	set_bar_state(bar_state)

def set_cumulative_leds(leds):
	bar_state = 2**leds - 1
	set_bar_state(bar_state)

# used for showing setting value
def leds_stack(leds, blinking=False, blinking_freq=1, fraction_on=0.25):
	global BLINK_STATE
	
	if not blinking:
		set_cumulative_leds(leds)
		return
	
	wait_time = 1 / blinking_freq
	now = time.time()
	
	on = ((now % wait_time) / wait_time) < fraction_on
	
	if BLINK_STATE == on:
		return
	
	if on:
		set_cumulative_leds(leds)
		BLINK_STATE = True
	else:
		blackout()
		BLINK_STATE = False
	
# used when setting state switches
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

def determine_output(setting_nr, setting_value, time_last_setting_press, time_last_measurement_press, time_last_setting_changed):
	now = time.time()
	
	# choosing setting mode
	if now - time_last_setting_press < 2:
		set_single_led(setting_nr + 1)
		return
	
	# determine setting is old
	old_value = now - time_last_setting_changed > 2
	
	match setting_nr:
		case 0:
			if old_value:
				leds_stack(max(int(10 * setting_value), 1), blinking=True)
			else:
				reverse = not setting_value
				swipe_full(reverse=reverse)
		
		case 1:
			leds_stack(int(setting_value + 1), blinking=old_value)
		
		case 2:
			bpm_min = 60
			bpm_max = 200
			bpm_diff = bpm_max - bpm_min
			fraction = (setting_value - bpm_min) / bpm_diff
			tens = int(round(10 * fraction, 0))
			tens = max(1, min(10, tens)) # stay within bounds [0, 10]
			leds_stack(tens, blinking=old_value)

		case 3:
			leds_stack(int(round(10 * setting_value, 0)), blinking=old_value)
		
		case 4:
			leds_stack(int(round(10 * setting_value, 0)), blinking=old_value)
		
		case 5:
			leds_stack(int(setting_value), blinking=old_value)
	
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
