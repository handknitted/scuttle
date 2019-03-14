import RPi.GPIO as GPIO


# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

_MOTOR_1_POS = 7
_MOTOR_1_NEG = 8
_MOTOR_2_POS = 9
_MOTOR_2_NEG = 10


MOTOR_PINS = (_MOTOR_1_POS, _MOTOR_1_NEG, _MOTOR_2_POS, _MOTOR_2_NEG)

FORWARD = (1, 0, 1, 0)
BACKWARD = (0, 1, 0, 1)
SPIN_LEFT = (0, 1, 1, 0)
SPIN_RIGHT = (1, 0, 0, 1)


def setup_gpio():
    for pin in MOTOR_PINS:
        GPIO.setup(pin, GPIO.OUT)


def motors_on(movement):
    for index, pin in enumerate(MOTOR_PINS):
        GPIO.output(pin, movement[index])


def motors_off():
    GPIO.cleanup()


setup_gpio()
