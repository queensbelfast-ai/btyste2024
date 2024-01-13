import time
import Jetson.GPIO as GPIO
import evdev

# Function to find an Xbox controller connected to the system
def find_xbox_controller():
    # List all connected input devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    # Check if any of these devices is an Xbox controller and return its path
    for device in devices:
        if "Generic X-Box pad" in device.name:
            return device.path
    # Return None if no Xbox controller is found
    return None

# Define the GPIO pins on the Jetson Nano that will be used for LEDs
led_pins = [11, 13, 15, 16, 18, 22, 29, 31, 32, 33]
# Calculate the number of LEDs based on the number of pins defined
num_leds = len(led_pins)

# Set up GPIO pins
GPIO.setmode(GPIO.BOARD)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

# Find the Xbox controller
event_device_path = find_xbox_controller()

try:
    # Initialize the Xbox controller device
    xbox_series_controller = evdev.InputDevice(event_device_path)
    print(f"Xbox Series controller found: {xbox_series_controller.name}")
    
    # Read input events in a loop
    for event in xbox_series_controller.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            # Handle right trigger (RT) events
            if event.code == evdev.ecodes.ABS_RZ:
                rt_val = event.value
                # Calculate number of LEDs to light up based on RT value
                rt_leds = int((rt_val / 1023.0) * num_leds / 2)
                rt_leds = max(0, min(rt_leds, num_leds // 2))

                # Update the state of the LEDs based on the RT value
                for i, pin in enumerate(led_pins[:num_leds // 2]):
                    GPIO.output(pin, GPIO.HIGH if i < rt_leds else GPIO.LOW)

            # Handle left trigger (LT) events
            elif event.code == evdev.ecodes.ABS_Z:
                lt_val = event.value
                # Calculate number of LEDs to light up based on LT value
                lt_leds = int((lt_val / 1023.0) * num_leds / 2)
                lt_leds = max(0, min(lt_leds, num_leds // 2))

                # Update the state of the LEDs based on the LT value
                for i, pin in enumerate(led_pins[num_leds // 2:]):
                    GPIO.output(pin, GPIO.HIGH if i < lt_leds else GPIO.LOW)

except FileNotFoundError:
    # Handle error if Xbox controller is not found
    print(f"Error: Could not find the specified event device at {event_device_path}")
except PermissionError:
    # Handle error if there is a permission issue
    print(f"Error: Permission denied. Try running the script with elevated privileges using 'sudo'.")
except KeyboardInterrupt:
    # Handle script termination by the user
    print("\nScript terminated by user. Cleaning up...")
finally:
    # Clean up GPIO to ensure all pins are turned off
    GPIO.cleanup()
    print("GPIO cleanup complete.")
