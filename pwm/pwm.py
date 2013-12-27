__author__ = 'paul'

#!/usr/bin/python

import time
import math
import i2c
import util


class Pwm:
    """Class for manipulating the servo control board"""
    # there will be two boards in total
    b1 = None  # board 1
    log = None

    # Registers/etc.
    __SUBADR1 = 0x02
    __SUBADR2 = 0x03
    __SUBADR3 = 0x04
    __MODE1 = 0x00
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALLLED_ON_L = 0xFA
    __ALLLED_ON_H = 0xFB
    __ALLLED_OFF_L = 0xFC
    __ALLLED_OFF_H = 0xFD

    # Min Max servo values
    __SERVO_MIN = 200
    __SERVO_MAX = 500

    def __init__(self):
        self.b1 = i2c.I2cBus(0x40)
        self.b1address = 0x40
        self.log = util.logger
        self.log.debug('Resetting PCA9685 controller')
        self.b1.write_byte(self.__MODE1, 0x00)
        time.sleep(0.005)
        self.set_freq(60)

    def set_freq(self, freq):
        """Sets the PWM frequency"""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        self.log.debug('Setting PWM frequency to: ' + str(freq) + 'Hz')
        self.log.debug('Estimated pre-scale: ' + str(prescaleval))
        prescale = math.floor(prescaleval + 0.5)
        self.log.debug('Final pre-scale: ' + str(prescale))

        oldmode = self.b1.read_unsigned_byte(self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10             # sleep
        self.b1.write_byte(self.__MODE1, newmode)        # go to sleep
        self.b1.write_byte(self.__PRESCALE, int(math.floor(prescale)))
        self.b1.write_byte(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.b1.write_byte(self.__MODE1, oldmode | 0x80)

    def set_servo_pulse(self, channel, pulse_start, pulse_end):
        """Sets a single servo PWM channel where pulseStart is typical 0 and pulseEnd is the end of the pulse"""
        pulse_length = pulse_end - pulse_start
        if (pulse_length > self.__SERVO_MIN) and (pulse_length < self.__SERVO_MAX):
            self.b1.write_byte(self.__LED0_ON_L + 4 * channel, pulse_start & 0xFF)
            self.b1.write_byte(self.__LED0_ON_H + 4 * channel, pulse_start >> 8)
            self.b1.write_byte(self.__LED0_OFF_L + 4 * channel, pulse_end & 0xFF)
            self.b1.write_byte(self.__LED0_OFF_H + 4 * channel, pulse_end >> 8)
        else:
            self.log.error('pulse length exceeds servo limits ' + str(pulse_length))




