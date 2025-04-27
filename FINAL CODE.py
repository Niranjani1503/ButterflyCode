# Write your code here :-)

#final code

from machine import Pin, PWM
import neopixel
import time

# === NeoPixel setup ===
num_pixels = 16
np = neopixel.NeoPixel(Pin(5), num_pixels)
left_color = (0, 0, 225)    #E initial blue
right_color = (225, 0, 0)   # initial red

# === Servo setup ===
servo = PWM(Pin(15), freq=50)

# === Reed switch setup ===
reed = Pin(14, Pin.IN, Pin.PULL_UP)  # Change to your reed switch pin

def run_cycle():
    global left_color, right_color

    # Move servo slowly from 0° to ~90°
    for d in range(25, 125):
        servo.duty(d)
        time.sleep(0.05)

    # Light up LEDs toward center
    for i in range(4):
        np[i] = left_color
        np[num_pixels -  1 - i] = right_color
        np.write()
        time.sleep(0.1)

    # Move servo slowly back from ~90° to 0°
    for d in range(125, 24, -1):
        servo.duty(d)
        time.sleep(0.05)

    # Turn off LEDs in reverse
    for i in reversed(range(8)):
        np[i] = (0, 0, 0)
        np[num_pixels - 1 - i] = (0, 0, 0)
        np.write()
        time.sleep(0.1)

    # Swap colors for next cycle
    left_color, right_color = right_color, left_color

# === Main loop ===
while True:
    if reed.value() == 0:  # Triggered when magnet is near (assuming active-low)
        for i in range(3):  # Run 3 cycles
            run_cycle()
    time.sleep(0.1)
