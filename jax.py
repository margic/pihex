import ConfigParser
from client import stompclient
from servo.pwm import Pwm
from sequencer import controller
import util

__author__ = 'Paul'

""" This is the main start point for the JAX robot
    This starts the client and control system
"""
log = util.logger


def main():
    log.info('Starting the JAX robot controller')

    # load config properties
    config = ConfigParser.ConfigParser()
    config.read('config.cfg')
    remote_queue_host = config.get('RemoteQueue', 'host')
    remote_queue_port = config.getint('RemoteQueue', 'port')
    remote_queue_username = config.get('RemoteQueue', 'username')
    remote_queue_password = config.get('RemoteQueue', 'password')
    remote_receive_queue = config.get('RemoteQueue', 'receive_queue')
    remote_send_queue = config.get('RemoteQueue', 'send_queue')

    # start the stomp client
    stomp_client = stompclient.StompClient(remote_queue_host, remote_queue_port, remote_queue_username, remote_queue_password)
    stomp_client.start_listener(remote_receive_queue)

    stomp_client.send_signon(remote_send_queue)

    pwm = None

    loop = True
    while loop:
        value = int(raw_input('Enter pulse length: '))
        if value == -1:
            loop = False
        else:
            if pwm is None:
                pwm = Pwm()
            pwm.set_servo_pulse(0, 0, value)
            pwm.set_servo_pulse(1, 0, value)

    #controller.start()

if __name__ == "__main__":
    main()