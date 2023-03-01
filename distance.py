import logging
import RPi.GPIO as GPIO
import time

logging.basicConfig(level=logging.INFO)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin_trigger = 27
pin_echo = 22
pin_warning = 17

WARNING_DISTANCE = 0.2
TEN_MILLISECONDS = 0.010
TEN_MICROSECONDS = 0.00001
PING_DURATION = TEN_MICROSECONDS * 5.0
SPEED_OF_SOUND = 343.26  # metres per second
# I think that the adjustment factor needs to take into account
# spread when we're calculating from the end of a sound pulse rather than the leading edge
EXPERIMENTAL_ADJUSTMENT_FACTOR = 24.0 / 37.01#.0#60.0 / 285.0

logging.info("Ultrasonic measurement")

GPIO.setup(pin_warning, GPIO.OUT)
GPIO.setup(pin_trigger, GPIO.OUT)
GPIO.setup(pin_echo, GPIO.IN)


class DistanceSensor(object):

    def __init__(self, warning_distance=0.2):
        self.warning_distance = warning_distance

    def get_distance(self):

            GPIO.output(pin_trigger, False)
            time.sleep(TEN_MILLISECONDS)

            echo_sensed = False
            GPIO.output(pin_trigger, True)
            start_time = time.time()
            # TODO this is all very well but it would be far better to trigger from the up rather than the down.
            # TODO Echoes and wide spread reflection ae causing issues with close distances.
            time.sleep(PING_DURATION)
            GPIO.output(pin_trigger, False)

            while not echo_sensed:
                echo_sensed = GPIO.input(pin_echo)

            while echo_sensed:
                echo_sensed = GPIO.input(pin_echo)

            finish_time = time.time()

            # correct start_time for the duration of the ping
            start_time -= PING_DURATION
            if finish_time - start_time >= 0.04:
                logging.info("Too close!")
                finish_time = start_time

            round_trip_elapsed_time = finish_time - start_time

            # round trip distance = speed of sound * elapsed time
            round_trip_distance = round_trip_elapsed_time * SPEED_OF_SOUND * EXPERIMENTAL_ADJUSTMENT_FACTOR
            object_distance = round_trip_distance / 2
            logging.info("Distance: %.5f m" % object_distance)
            if object_distance < self.warning_distance:
                GPIO.output(17, True)
            else:
                GPIO.output(17, False)
            time.sleep(TEN_MILLISECONDS)
            return object_distance


if __name__ == '__main__':
    try:
        distance_sensor = DistanceSensor()
        while True:
            distance_ahead = distance_sensor.get_distance()
            print("Distances: ahead: %.5f m" % (
                distance_ahead))

    except KeyboardInterrupt:
        GPIO.cleanup()


