import os
from daemon.runner import DaemonRunner
import pydevd
import signal
from pihex import PiHex
import util

__author__ = 'paul'

pihex = PiHex()
daemon_runner = DaemonRunner(pihex)
daemon_runner.daemon_context.working_directory = os.getcwd()
# add our terminate method to the signal map
daemon_runner.daemon_context.signal_map[signal.SIGTERM] = pihex.terminate
daemon_runner.daemon_context.files_preserve = [util.file_handler.stream]
daemon_runner.do_action()
