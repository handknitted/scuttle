import logging

import RPi.GPIO as GPIO
from threading import Thread


logging.basicConfig(level=logging.INFO)


class Motors(object):

    pass


class ScuttleMotors(Motors):

    def __init__(self):
        self.old_movement = None
        # Set the GPIO modes
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        _MOTOR_1_POS = 7
        _MOTOR_1_NEG = 8
        _MOTOR_2_POS = 9
        _MOTOR_2_NEG = 10

        motor_pins = (_MOTOR_1_POS, _MOTOR_1_NEG, _MOTOR_2_POS, _MOTOR_2_NEG)
        self.PWM_PINS = []

        # How many times to turn the pin on and off each second
        frequency = 200
        # How long the pin stays on each cycle, as a percent
        duty_cycle = 50

        # Setting the duty cycle to 0 means the motors will not turn
        stop = 0

        self.FORWARD = (duty_cycle, 0, duty_cycle, 0)
        self.BACKWARD = (0, duty_cycle, 0, duty_cycle)
        self.SPIN_LEFT = (0, duty_cycle, duty_cycle, 0)
        self.SPIN_RIGHT = (duty_cycle, 0, 0, duty_cycle)
        self.STOP = (0, 0, 0, 0)

        for pin in motor_pins:
            GPIO.setup(pin, GPIO.OUT)
            pwm_pin = GPIO.PWM(pin, frequency)
            pwm_pin.start(stop)
            self.PWM_PINS.append(pwm_pin)

    def motors_change(self, move):
        # if we have no old movement then just start
        if self.old_movement is None:
            for index, pin in enumerate(self.PWM_PINS):
                pin.ChangeDutyCycle(move[index])
        else:
            # otherwise create threads to change the duty cycle smoothly
            running_threads = []
            for index, pin in enumerate(self.PWM_PINS):
                pass
                # create a thread for each pin to transition from old duty cycle to new duty cycle
                old_duty_cycle = self.old_movement[index]
                new_duty_cycle = move[index]
                logging.info('Transitioning pin %s from duty cycle %s to %s' %
                             (str(pin), str(old_duty_cycle), str(new_duty_cycle)))
                thread = Thread(target=self.change_duty_cycle, args=[pin, old_duty_cycle, new_duty_cycle])
                running_threads.append(thread)
                thread.start()
            for thread in running_threads:
                thread.join()
        self.old_movement = move

    @staticmethod
    def change_duty_cycle(pin, old_duy_cycle, new_duty_cycle):
        steps = 10
        # establish the difference in the duty cycles
        transition_size = new_duty_cycle - old_duy_cycle
        step_size = transition_size/steps
        # loop with a delay, stepping the duty cycle toward the new value evenly
        while steps > 0:
            steps -= 1
            old_duy_cycle += step_size
            pin.ChangeDutyCycle(old_duy_cycle)
            time.sleep(0.01)

    def forward(self):
        self.motors_change(self.FORWARD)

    def backward(self):
        self.motors_change(self.BACKWARD)

    def spin_left(self):
        self.motors_change(self.SPIN_LEFT)

    def spin_right(self):
        self.motors_change(self.SPIN_RIGHT)

    def stop(self):
        self.motors_change(self.STOP)


if __name__ == '__main__':
    import time
    scuttle = ScuttleMotors()
    for movement in (scuttle.forward,
                     scuttle.spin_left,
                     scuttle.backward,
                     scuttle.spin_right,
                     scuttle.stop):
        movement()
        time.sleep(5)
