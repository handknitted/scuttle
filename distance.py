import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin_trigger = 27
pin_echo = 22
pin_warning = 17

WARNING_DISTANCE = 0.2
HALF_A_SECOND = 0.5
TEN_MICROSECONDS = 0.00001
PING_DURATION = TEN_MICROSECONDS * 5.0
SPEED_OF_SOUND = 343.26  # metres per second
# I think that the adjustment factor needs to take into account
# spread when we're calculating from the end of a sound pulse rather than the leading edge
EXPERIMENTAL_ADJUSTMENT_FACTOR = 24.0 / 37.01#.0#60.0 / 285.0

print("Ultrasonic measurement")

GPIO.setup(pin_warning, GPIO.OUT)
GPIO.setup(pin_trigger, GPIO.OUT)
GPIO.setup(pin_echo, GPIO.IN)


def get_distance():

        GPIO.output(pin_trigger, False)
        time.sleep(HALF_A_SECOND)

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
            print("Too close!")
            finish_time = start_time

        round_trip_elapsed_time = finish_time - start_time

        # round trip distance = speed of sound * elapsed time
        round_trip_distance = round_trip_elapsed_time * SPEED_OF_SOUND * EXPERIMENTAL_ADJUSTMENT_FACTOR
        object_distance = round_trip_distance / 2
        print("Distance: %.5f m" % object_distance)
        if object_distance < WARNING_DISTANCE:
            GPIO.output(17, True)
        else:
            GPIO.output(17, False)
        time.sleep(HALF_A_SECOND * 2)
        return object_distance


if __name__ == '__main__':
    try:
        while True:
            distance_ahead = get_distance()
            print("Distances: ahead: %.5f m" % (
                distance_ahead))

    except KeyboardInterrupt:
        GPIO.cleanup()


