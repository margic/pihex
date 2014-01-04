import ConfigParser
from sequencer.controller import Controller
import util

__author__ = 'Paul'


class PiHex():

    def __init__(self):
        self.log = util.logger
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/var/run/pihex/pihex.pid'
        self.pidfile_timeout = 5
        # load config properties
        config = ConfigParser.ConfigParser()
        config.read('config/settings.cfg')
        self.queue_config = dict()
        self.queue_config['remote_queue_host'] = config.get('RemoteQueue', 'host')
        self.queue_config['remote_queue_port'] = config.getint('RemoteQueue', 'port')
        self.queue_config['remote_queue_username'] = config.get('RemoteQueue', 'username')
        self.queue_config['remote_queue_password'] = config.get('RemoteQueue', 'password')
        self.queue_config['remote_receive_queue'] = config.get('RemoteQueue', 'receive_queue')
        self.queue_config['remote_send_queue'] = config.get('RemoteQueue', 'send_queue')

    def run(self):
        self.log.info('Starting the JAX robot controller')
        # start the controller
        controller = Controller(self.queue_config)
        #controller.start()


def main():
    pihex = PiHex()
    pihex.run()

if __name__ == '__main__':
    main()