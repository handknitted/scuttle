import logging
import time
from distance import DistanceSensor, CheckTooSoon
from motor import ScuttleMotors


logging.basicConfig(level=logging.INFO)

minimum_distance = 0.3

distance_sensor = DistanceSensor(warning_distance=minimum_distance)

scuttle = ScuttleMotors()
try:

    while True:
        # check distance in front
        try:
            if distance_sensor.is_clear_forward():
                logging.info("Clear forward")
                # go straight
                new_movement = scuttle.forward()
            else:
                logging.info("Obstacle within %sm. Turning." % minimum_distance)
                # try turning
                new_movement = scuttle.spin_left()

        except CheckTooSoon as e:
            # ignore and loop again
            time.sleep(0.05)
            pass
except KeyboardInterrupt:

    scuttle.stop()
    raise SystemExit
