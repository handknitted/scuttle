import mag3110
from distance import get_distance
from motor import FORWARD, BACKWARD, SPIN_RIGHT, SPIN_LEFT, motors_on, motors_off

minimum_distance = 0.3


def is_clear_forward():
    return get_distance() > minimum_distance


while True:
    # check distance in front
    if is_clear_forward():
        # go straight
        motors_on(FORWARD)
    else:
        # try turning
        motors_on(SPIN_LEFT)
