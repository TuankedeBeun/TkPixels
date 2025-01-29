# Summary
This is the code for controlling the NeoPixel.

To run one of the scripts, type `sudo python3 Programmin/Python/do_rainbow.py`.
If the script stops or fails, the LEDs will stay on. 
In that case, run `sudo python3 Programmin/Python/ledoff.py`.

# Prerequisites
Install Raspberry OS using Imager:
- Put the SD card in
- Format SD card
- Install Imager
- Open Imager and install Raspberry PI 3B on the SD card
- Customize to set WIFI, etc.
- After installation is complete, put the SD card into the Raspberry PI
- Start the Raspberry PI by powering it

Install required Python modules:
- Install neopixel and board modules by running `sudo pip3 install adafruit-circuitpython-neopixel --break-system-packages`

Test