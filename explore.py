import atexit
import logging
from enum import Enum
import mag3110
from distance import DistanceSensor
from motor import FORWARD, BACKWARD, SPIN_RIGHT, SPIN_LEFT, motors_on, motors_off


class Movement(Enum):

    Forward = FORWARD
    Backward = BACKWARD
    SpinLeft = SPIN_LEFT
    SpinRight = SPIN_RIGHT


logging.basicConfig(level=logging.INFO)

minimum_distance = 0.3

distance_sensor = DistanceSensor(warning_distance=minimum_distance)


def is_clear_forward():
    return distance_sensor.get_distance() > minimum_distance


try:
    current_movement = None
    new_movement = None

    while True:
        # check distance in front
        if is_clear_forward():
            logging.info("Clear forward")
            # go straight
            new_movement = Movement.Forward
        else:
            logging.info("Obstacle within %sm. Turning.")
            # try turning
            new_movement = Movement.SpinLeft
            motors_on(new_movement.value)

        if current_movement != new_movement:
            motors_on(new_movement.value)
except KeyboardInterrupt:

    motors_off()
    raise SystemExit
