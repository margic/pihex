from abc import abstractmethod

__author__ = 'paul'


class PwmSender:

    def __init__(self):
        pass

    @abstractmethod
    def set_servo_pulse(self, pulse_item):
        """
        @param pulse_item: the pulse details
        @type pulse_item: tuple
        """
        pass