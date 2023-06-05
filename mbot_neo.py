"""
    Python Editor: https://python.mblock.cc/
    Needs mLink2 installed on the computer: https://www.mblock.cc/en/download/mlink/
    Works in upload mode only, at least for me
    Author: Prabhjot Singh
"""


import cyberpi  # https://education.makeblock.com/help/mblock-python-editor-python-api-documentation-for-cyberpi/
import mbot2    # https://education.makeblock.com/help/mblock-python-editor-apis-for-extension-boards/


class mbot_neo:
    def __init__(self):
        self.speed = 50     # RPM
        self.time = 1.0     # For movement (seconds)
        self.distance = 16  # For movement (cm)


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


    def print_line(self, text):
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
                self.print_line("Moving forward at " + str(speed) + " RPM for " + str(time) + " seconds")
                mbot2.forward(speed, time)
            else:
                self.print_line("Moving forward at " + str(speed) + " RPM for " + str(distance) + " cm")
                mbot2.straight(distance, speed)
        elif direction == "backward":
            if mode == "time":
                self.print_line("Moving backward at " + str(speed) + " RPM for " + str(time) + " seconds")
                mbot2.backward(speed, time)
            else:
                self.print_line("Moving backward at " + str(speed) + " RPM for " + str(distance) + " cm")
                distance = -1 * distance
                mbot2.straight(distance, speed)
        elif direction == "left":
            if mode == "time":
                self.print_line("Turning left at " + str(speed) + " RPM for " + str(time) + " seconds")
                mbot2.turn_left(speed, time)
            else:
                # Left means turn counter-clockwise
                self.print_line("Turning left at " + str(speed) + " RPM for " + str(distance) + " degrees")
                distance = -1 * distance
                mbot2.turn(distance, speed)
        elif direction == "right":
            if mode == "time":
                self.print_line("Turning right at " + str(speed) + " RPM for " + str(time) + " seconds")
                mbot2.turn_right(speed, time)
            else:
                self.print_line("Turning right at " + str(speed) + " RPM for " + str(distance) + " degrees")
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


@cyberpi.event.is_press("b")
def actions():
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

mbot = mbot_neo()
mbot.print_line("Press B (play) button to start")
