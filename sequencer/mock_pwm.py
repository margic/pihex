from sequencer.pwm_sender import PwmSender
import util

__author__ = 'paul'


class MockPwm(PwmSender):
    def set_servo_pulse(self, pulse_item):
        log = util.logger
        log.debug('Mock sender pulse item %s' % (pulse_item,))