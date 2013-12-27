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
                self.log.debug('I2C: Wrote ' + str(value) + ' to register ' + str(reg))
        except IOError:
            self.log.error('Error accessing ' + str(self.address) + ': Check your I2C address')
            return -1

    def read_unsigned_byte(self, reg):
        """Read an unsigned byte from the I2C device"""
        try:
            result = self.bus.read_byte_data(self.address, reg)
            if self.log.isEnabledFor(logging.DEBUG):
                self.log.debug('I2C: Device ' + str(self.address) + ' returned ' + str(result & 0xFF) + ' from reg ' + str(reg))
            return result
        except IOError:
            self.log.error('Error reading i2c device ' + str(self.address))
            return -1