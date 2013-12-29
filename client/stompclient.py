import stomp
import util

__author__ = 'paul'

log = util.logger


class QueueListener(object):

    def on_error(self, headers, message):
        log.debug('received an error %s' % message)

    def on_message(self, headers, message):
        log.debug('received a message %s' % message)


class StompClient:

    def __init__(self, host, port, username, password):
        """
        Initializes the stomp client with host params
        @param host:
        @param port:
        @param username:
        @param password:
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.conn = stomp.Connection

    def start_listener(self, queue):
        """
        Starts the stomp client and starts listening for incoming messages
        @param self:
        @param queue:
        """
        conn = stomp.Connection([(self.host, self.port)])
        conn.set_listener('', QueueListener())
        conn.start()
        conn.connect(self.username, self.password)

        conn.subscribe(destination=queue, id=1, ack='auto')
        self.conn = conn

    def send_signon(self, queue):
        """
        Send the sign on to the main robot control server
        @param queue:
        """
        self.conn.send(destination=queue, body='{"signon":true}')