import RPi.GPIO as GPIO


# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

_MOTOR_1_POS = 7
_MOTOR_1_NEG = 8
_MOTOR_2_POS = 9
_MOTOR_2_NEG = 10


MOTOR_PINS = (_MOTOR_1_POS, _MOTOR_1_NEG, _MOTOR_2_POS, _MOTOR_2_NEG)
PWM_PINS = []



# How many times to turn the pin on and off each second
Frequency = 200
# How long the pin stays on each cycle, as a percent
duty_cycle = 50

# Setting the duty cycle to 0 means the motors will not turn
Stop = 0

FORWARD = (duty_cycle, 0, duty_cycle, 0)
BACKWARD = (0, duty_cycle, 0, duty_cycle)
SPIN_LEFT = (0, duty_cycle, duty_cycle, 0)
SPIN_RIGHT = (duty_cycle, 0, 0, duty_cycle)


def setup_gpio():
    for pin in MOTOR_PINS:
        GPIO.setup(pin, GPIO.OUT)
        pwm_pin = GPIO.PWM(pin, Frequency)
        pwm_pin.start(Stop)
        PWM_PINS.append(pwm_pin)


def motors_on(movement):
    for index, pin in enumerate(PWM_PINS):
        pin.ChangeDutyCycle(movement[index])


def motors_off():
    GPIO.cleanup()


setup_gpio()

if __name__ == '__main__':
    import time
    for movement in (FORWARD, SPIN_LEFT, BACKWARD, SPIN_RIGHT):
        motors_on(movement)
        time.sleep(1)

    motors_off()
