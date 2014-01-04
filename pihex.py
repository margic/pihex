import ConfigParser
from client.stompclient import StompClient
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

    def run(self):
        self.init_robot()

    def init_robot(self):
        self.log.info('Starting the JAX robot controller')

        # load config properties
        config = ConfigParser.ConfigParser()
        config.read('config/settings.cfg')
        remote_queue_host = config.get('RemoteQueue', 'host')
        remote_queue_port = config.getint('RemoteQueue', 'port')
        remote_queue_username = config.get('RemoteQueue', 'username')
        remote_queue_password = config.get('RemoteQueue', 'password')
        remote_receive_queue = config.get('RemoteQueue', 'receive_queue')
        remote_send_queue = config.get('RemoteQueue', 'send_queue')

        # start the controller
        controller = Controller()
        #controller.set_pwm_sender(AdaPwm())
        controller.start()

        # start the stomp client
        stomp_client = StompClient(remote_queue_host, remote_queue_port, remote_queue_username, remote_queue_password)
        stomp_client.set_controller(controller)
        stomp_client.start_listener(remote_receive_queue)

        stomp_client.send_signon(remote_send_queue)
