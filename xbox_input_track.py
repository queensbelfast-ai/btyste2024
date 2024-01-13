import evdev

def find_xbox_controller():
    # Create a list of all connected input devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    # Search through the devices to find one with a name matching an Xbox controller
    for device in devices:
        if "Generic X-Box pad" in device.name:
            # Return the path of the Xbox controller if found
            return device.path
    # Return None if no Xbox controller is found
    return None

# Store the path of the Xbox controller
event_device_path = find_xbox_controller()

try:
    # Initialize the Xbox controller device using its path
    xbox_series_controller = evdev.InputDevice(event_device_path)
    # Confirm the Xbox controller is connected and display its name
    print(f"Xbox Series controller found: {xbox_series_controller.name}")

    # Continuously read input events from the controller
    for event in xbox_series_controller.read_loop():
        # Filter for absolute axis events (like joystick movement)
        if event.type == evdev.ecodes.EV_ABS:
            # Check if the event is for the X-axis (left joystick horizontal)
            if event.code == evdev.ecodes.ABS_X:
                print(f"X-axis event at {event.timestamp()}, {evdev.ecodes.ABS[event.code]}: {event.value}")
            # Check if the event is for the left trigger (Z-axis)
            elif event.code == evdev.ecodes.ABS_Z:
                print(f"Left trigger event at {event.timestamp()}, {evdev.ecodes.ABS[event.code]}: {event.value}")
            # Check if the event is for the right trigger (RZ-axis)
            elif event.code == evdev.ecodes.ABS_RZ:
                print(f"Right trigger event at {event.timestamp()}, {evdev.ecodes.ABS[event.code]}: {event.value}")

# Handle the exception if the Xbox controller is not found
except FileNotFoundError:
    print(f"Error: Could not find the specified event device at {event_device_path}")
# Handle the exception if there is a permission error (common in Linux)
except PermissionError:
    print(f"Error: Permission denied. Try running the script with elevated privileges using 'sudo'.")
# Handle any other exceptions that may occur
except Exception as e:
    print(f"Error: {e}")
