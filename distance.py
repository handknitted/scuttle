import RPi.GPIO as GPIO
import time


ahead_pin_trigger = 17
ahead_pin_echo = 18
DISTANCE_AHEAD = (ahead_pin_trigger, ahead_pin_echo)
astern_pin_trigger = 27
astern_pin_echo = 22
DISTANCE_ASTERN = (astern_pin_trigger, astern_pin_echo)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


PRE_TRIGGER_DELAY = 0.05
TEN_MICROSECONDS = 0.00001
PING_DURATION = TEN_MICROSECONDS * 5.0
SPEED_OF_SOUND = 343.26  # metres per second


GPIO.setup(ahead_pin_trigger, GPIO.OUT)
GPIO.setup(astern_pin_trigger, GPIO.OUT)
GPIO.setup(ahead_pin_echo, GPIO.IN)
GPIO.setup(astern_pin_echo, GPIO.IN)


def get_distance(pins):
    pin_trigger = pins[0]
    pin_echo = pins[1]
    GPIO.output(pin_trigger, False)
    time.sleep(PRE_TRIGGER_DELAY)
    GPIO.output(pin_trigger, True)
    time.sleep(TEN_MICROSECONDS)
    GPIO.output(pin_trigger, False)

    start_time = time.time()

    while GPIO.input(pin_echo) == 0:
        start_time = time.time()

    stop_time = time.time()
    while GPIO.input(pin_echo) == 1:
        stop_time = time.time()

    if stop_time - start_time >= 0.04:
        print("Too close!")

    round_trip_elapsed_time = stop_time - start_time

    # round trip distance = speed of sound * elapsed time
    round_trip_distance = round_trip_elapsed_time * SPEED_OF_SOUND
    object_distance = round_trip_distance / 2
    return object_distance


if __name__ == '__main__':
    try:
        while True:
            distance_ahead = get_distance(DISTANCE_AHEAD)
            distance_astern = get_distance(DISTANCE_ASTERN)
            print("Distances: ahead: %.5f m, astern: %.5f m, total %.5f m" % (
                distance_ahead, distance_astern, (distance_ahead + distance_astern)))

    except KeyboardInterrupt:
        GPIO.cleanup()


