"""
    Python Editor: https://python.mblock.cc/
        Needs mLink2 installed on the computer: https://www.mblock.cc/en/download/mlink/
        Works in upload mode only, which uses MicroPython.
            MicroPython supports limited number of libraries: https://docs.micropython.org/en/latest/library/index.html
        Live mode uses Python 3 but devices only run code when connected to the computer
    Author: Prabhjot Singh
"""


import time
import mbot2    # https://education.makeblock.com/help/mblock-python-editor-apis-for-extension-boards/
import cyberpi  # https://education.makeblock.com/help/mblock-python-editor-python-api-documentation-for-cyberpi/
# Sensors: https://education.makeblock.com/help/mblock-python-editor-apis-for-mbuild-modules/

# MicroPython libraries
# https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html
import urequests as requests # only works with http requests, not https (OSError: [Errno 12] ENOMEM)


WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"


class mbot_neo:
    def __init__(self):
        self.speed = 50     # RPM
        self.time = 1.0     # For movement (seconds)
        self.distance = 16  # For movement (cm)

        # Connect to WiFi
        self.print("Connecting to WiFi...")
        while not cyberpi.wifi.is_connect():
            cyberpi.wifi.connect(WIFI_SSID, WIFI_PASSWORD)
            if cyberpi.wifi.is_connect():
                cyberpi.audio.play("level-up")
                break
            time.sleep(1)
            self.print("Unable to connect to WiFi. Retrying...")
        self.print("Connected to WiFi")


    """
        Setters
    """
    # Change default speed
    def set_speed(self, speed):
        if speed < 0:
            speed = self.speed
        elif speed > 200:
            speed = 200
    
        self.speed = speed

    # Change default time
    def set_time(self, time):
        if time < 0:
            time = self.time
    
        self.time = time

    # Change default distance
    def set_distance(self, distance):
        if distance < 0:
            distance = self.distance
    
        self.distance = distance


    # Prints text on the CyberPi screen
    # Clears the screen by default
    def print(self, text, clear = True, center = False):
        if clear:
            cyberpi.display.clear()
        cyberpi.console.println(text)


    # Moves in the specified direction at the specified speed for the specified time or distance
    # Directions: forward, backward, left, right
    # Speed: 0 - 200 RPM
    # Time: seconds
    # Distance: cm (for forward/backward) or degrees (for left/right). Negative values for left and backward.
    def _move(self, speed, time, distance, direction):
        # Check for invalid speed
        if speed == None or speed < 0:
            speed = self.speed
        elif speed > 200:
            speed = 200 # Max speed is 200 RPM

        # Determine mode: time or distance
        mode = "time"
        if time == None:
            if distance != None:
                mode = "distance"
                if distance < 0:
                    distance = self.distance
            else:
                time = self.time

        # Move forever until a stop command is given
        elif time <= 0:
            time = None
        
        if direction == "forward":
            if mode == "time":
                self.print("Moving forward at " + str(speed) + " RPM for " + str(time) + " seconds")
                mbot2.forward(speed, time)
            else:
                self.print("Moving forward at " + str(speed) + " RPM for " + str(distance) + " cm")
                mbot2.straight(distance, speed)
        elif direction == "backward":
            if mode == "time":
                self.print("Moving backward at " + str(speed) + " RPM for " + str(time) + " seconds")
                mbot2.backward(speed, time)
            else:
                self.print("Moving backward at " + str(speed) + " RPM for " + str(distance) + " cm")
                distance = -1 * distance
                mbot2.straight(distance, speed)
        elif direction == "left":
            if mode == "time":
                self.print("Turning left at " + str(speed) + " RPM for " + str(time) + " seconds")
                mbot2.turn_left(speed, time)
            else:
                # Left means turn counter-clockwise
                self.print("Turning left at " + str(speed) + " RPM for " + str(distance) + " degrees")
                distance = -1 * distance
                mbot2.turn(distance, speed)
        elif direction == "right":
            if mode == "time":
                self.print("Turning right at " + str(speed) + " RPM for " + str(time) + " seconds")
                mbot2.turn_right(speed, time)
            else:
                self.print("Turning right at " + str(speed) + " RPM for " + str(distance) + " degrees")
                mbot2.turn(distance, speed)


    """
    Moves at speed (0 - 200 RPM) for either time (seconds) or distance (cm)
    For turns, distance is used as an angle (degrees)
    Moves forever if time of 0 or less is given
    If no speed is given, uses default speed of 50 RPM
    If no time is given, uses distance
    If neither time nor distance is given, uses default time of 1 second
    """
    def move_forward(self, speed = None, time = None, distance = None):
        self._move(speed, time, distance, "forward")

    def move_backward(self, speed = None, time = None, distance = None):
        self._move(speed, time, distance, "backward")

    def turn_left(self, speed = None, time = None, angle = None):
        self._move(speed, time, angle, "left")

    def turn_right(self, speed = None, time = None, angle = None):
        self._move(speed, time, angle, "right")

    def stop(self):
        mbot2.stop()


# Test all movement functions
@cyberpi.event.is_press("b")
def move_actions():
    mbot.move_forward()
    mbot.turn_left()
    mbot.turn_right()
    mbot.move_backward()
    mbot.move_forward(150, 0.5, 5)
    mbot.turn_left(25, 2, 5)
    mbot.turn_right(25, 2, 5)
    mbot.move_backward(150, 0.5, 5)
    mbot.move_forward(distance=32)
    mbot.turn_left(angle=90)
    mbot.turn_right(angle=90)
    mbot.move_backward(distance=32)


@cyberpi.event.is_press("a")
def http_request():
    mbot.print("Sending HTTP request...")
    response = requests.get("http://google.com")
    mbot.print(" ", False)
    mbot.print("Status code: " + str(response.status_code), False)
    if response.status_code == 200:
        mbot.print("Success!", False)


mbot = mbot_neo()
mbot.print("Press A to test HTTP request")
mbot.print(" ", False)
mbot.print("Press B to test movement", False)
