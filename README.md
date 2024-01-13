# BT Young Scientist 2024 Jetson Demo
This contains all the files used for QUB EEECS Jetson Demo showcased at BT Young Scientist 2024. It is designed to show concepts of mapping an Xbox Controller to data inputs that can be mapped to a voltage that will control a motor the Ninebot GoKart which the team plans to make autonomous.

### Requirements
To showcase this demo the following is required:
- Jetson Nano.
- Xbox Controller (Series X used at the event).
- PCB of LED array.
- Power Supply.

### Python3 libraries used
`pip3 install time`
`pip3 install evdev`
`pip3 install Jetson.GPIO`
`pip3 install curses`
### Overview
The files in this repo do the following:
-"xbox_control_visual.py" is used to show a GUI which displays the input in the user's terminal.
-"xbox_input_track.py" prints the controller input to the terminal.
-"led_array.py" will output the controller input to GPIO pins used to Brighten LEDs on the PCB.
