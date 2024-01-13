import evdev
import curses

# Function to find the Xbox controller by scanning connected devices
def find_xbox_controller():
    # List all connected input devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    # Search for a device with 'Generic X-Box pad' in its name
    for device in devices:
        if "Generic X-Box pad" in device.name:
            return device.path  # Return the path of the Xbox controller
    return None  # Return None if no Xbox controller is found

# Find the path of the Xbox controller
event_device_path = find_xbox_controller()

# Function to normalize the steering value to a range of -1.0 to 1.0
def normalize_steering_value(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) * 2 - 1

# Function to normalize a value to a range of 0 to 1
def normalize_value(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

# Function to draw a horizontal slider in the terminal
def draw_slider(stdscr, y, value, label, color_pair):
    slider_width = 60  # Define the width of the slider
    slider_fill = int(max(0, value) * slider_width)  # Calculate how much of the slider should be filled
    slider_display = f"[{'#' * slider_fill}{' ' * (slider_width - slider_fill)}]"  # Create the slider display
    # Add the slider text to the screen
    stdscr.addstr(y * 2, 0, f"{label}: {slider_display} {value:.5f}", curses.color_pair(1) | curses.A_BOLD)
    # Change the color of the filled part of the slider
    for i in range(slider_width):
        if i < slider_fill:
            stdscr.chgat(y * 2, i + len(label) + 3, 1, curses.color_pair(color_pair) | curses.A_BOLD)

# Function to draw a steering slider that can move left and right
def draw_steering_slider(stdscr, y, value, label):
    slider_width = 60  # Define the width of the slider
    slider_fill = int((value + 1) * slider_width / 2)  # Calculate the filled part of the slider based on steering value
    filled_char = '.'  # Character for filled part
    empty_char = '='  # Character for empty part
    slider_display = f"[{filled_char * slider_fill}{empty_char * (slider_width - slider_fill)}]"  # Create slider display
    stdscr.addstr(y * 2, 0, f"{label}: {slider_display} {value:.5f}")  # Add the slider text to the screen

# Function to set up color pairs for the terminal display
def setup_colors():
    curses.start_color()  # Initialize color functionality
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Set color pair 1
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Set color pair 2
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Set color pair 3

# Main function for handling input and updating the display
def main(stdscr):
    xbox_series_controller = evdev.InputDevice(event_device_path)  # Initialize the Xbox controller
    stdscr.clear()  # Clear the terminal screen
    stdscr.refresh()  # Refresh the screen to apply changes
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Set getch() to be non-blocking
    setup_colors()  # Set up colors for the display
    title = "Queen's AI Formula Student Demo"  # Title text
    stdscr.addstr(0, (curses.COLS - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)  # Display title

    # Main loop for handling controller input
    while True:
        event = xbox_series_controller.read_one()  # Read a single input event
        if event and event.type == evdev.ecodes.EV_ABS:  # Check if the event is an Absolute Axis event
            if event.code == evdev.ecodes.ABS_X:  # If the event is from the joystick X-axis
                normalized_x = normalize_steering_value(event.value, -32768, 32767)  # Normalize the X-axis value
                draw_steering_slider(stdscr, 1, normalized_x, "Steering Angle")  # Draw the steering slider
            elif event.code
