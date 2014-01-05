import os
from daemon.runner import DaemonRunner
from pihex import PiHex
import util

__author__ = 'paul'
pihex = PiHex()
daemon_runner = DaemonRunner(pihex)
daemon_runner.daemon_context.working_directory = os.getcwd()
daemon_runner.daemon_context.signal_map[15] = pihex.terminate
daemon_runner.daemon_context.files_preserve = [util.file_handler.stream]
daemon_runner.do_action()
