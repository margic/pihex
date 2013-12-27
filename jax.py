from pwm.pwm import Pwm
from sequencer import controller
import util

__author__ = 'Paul'

""" This is the main start point for the JAX robot
    This starts the client and control system
"""
log = util.logger


def main():
    log.info('Starting the JAX robot controller')

    pwm = None

    loop = True
    while loop:
        value = int(raw_input('Enter pulse length: '))
        if value == -1:
            loop = False
        else:
            if pwm is None:
                pwm = Pwm()
            pwm.set_servo_pulse(0, 0, value)
            pwm.set_servo_pulse(1, 0, value)

    #controller.start()

if __name__ == "__main__":
    main()