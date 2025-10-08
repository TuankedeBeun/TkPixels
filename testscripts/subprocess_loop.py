import subprocess
import time

def run_led_show():
    
    try:
        process = subprocess.Popen(["python3", "/home/tuanke/Programming/TkPixels/led_show.py"])

        while True:
            time.sleep(1)

            if process.poll() is not None:
                print("LED script crashed or exited. Restarting...")
                break

    except KeyboardInterrupt:
        print("Shutting down...")
        if process:
            process.kill()
        return

while True:
    run_led_show()