import ConfigParser
import os
import pydevd
import time
import signal
from sequencer.controller import Controller
import util

__author__ = 'Paul'


class PiHex():

    def __init__(self):
        self.log = util.logger
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = os.getcwd() + '/pihex.pid'
        self.pidfile_timeout = 5

        # the controller instance
        self.controller = None

    def terminate(self, signal_number, stack_frame):
        """
        Signal call back to allow the controller to shutdown on daemon termination
        @param signal_number:
        @param stack_frame:
        @return:
        """
        self.log.info('Terminating the robot controller %d' % signal_number)
        self.controller.stop()

    def run(self):
        self.log.info('Starting the JAX robot controller')
        # start the controller
        self.controller = Controller()
        self.controller.start()


def main():
    pihex = PiHex()
    signal.signal(signal.SIGTERM, pihex.terminate)
    signal.signal(signal.SIGINT, pihex.terminate)
    pihex.run()

if __name__ == '__main__':
    main()