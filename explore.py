import atexit
import logging

import mag3110
from distance import get_distance
from motor import FORWARD, BACKWARD, SPIN_RIGHT, SPIN_LEFT, motors_on, motors_off


class Movement(enum):

    Forward = FORWARD
    Backward = BACKWARD
    SpinLeft = SPIN_LEFT
    SpinRight = SPIN_RIGHT


logging.basicConfig(level=logging.INFO)

minimum_distance = 0.3


def is_clear_forward():
    return get_distance() > minimum_distance


try:
    current_movement = None
    new_movement = None

    while True:
        # check distance in front
        if is_clear_forward():
            logging.info("Clear forward")
            # go straight
            new_movement = Movement.Forward
            motors_on(FORWARD)
        else:
            logging.info("Obstacle within %sm. Turning.")
            # try turning
            new_movement = Movement.SpinLeft
            motors_on(SPIN_LEFT)

        if current_movement != new_movement:
            motors_on(new_movement)
            current_movement = new_movement
except KeyboardInterrupt:

    motors_off()
    raise SystemExit
