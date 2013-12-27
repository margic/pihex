import logging

__author__ = 'Paul'

#!/usr/bin/python

import util
import smbus


class I2cBus:

    def __init__(self, address):
        self.address = address
        self.log = util.logger
        # self.bus = smbus.SMBus(1); # Force I2C1 (512MB Pi's)
        self.bus = smbus.SMBus(1)

    def write_byte(self, reg, value):
        """Writes an 8-bit value to the specified register/address"""
        try:
            self.bus.write_byte_data(self.address, reg, value)
            if self.log.isEnabledFor(logging.DEBUG):
                self.log.debug('I2C: Wrote ' + value + ' to register ' + reg)
        except IOError:
            self.log.error('Error accessing ' + self.address + ': Check your I2C address')
            return -1

    def read_unsigned_byte(self, reg):
        """Read an unsigned byte from the I2C device"""
        try:
            result = self.bus.read_byte_data(self.address, reg)
            if self.log.isEnabledFor(logging.DEBUG):
                self.log.debug('I2C: Device ' + self.address + ' returned ' + result & 0xFF + ' from reg ' + reg)
            return result
        except IOError:
            self.log.error('Error reading i2c device ' + self.address)
            return -1