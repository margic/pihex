from client import StompClient
import util
import json
from multiprocessing import Pool

__author__ = 'Paul'

#   Controls the sequencing of firing of leg movement based in provided sequence
#   that is obtained from the rules system


class Controller():
    def __init__(self):
        self.servomap = None
        self.servcalibration = None
        self.stompclient = None
        self.log = util.logger

    def start(self):
        """
            starts the controller and prepares it for receiving sequences
        """
        self.log.info('Initializing the controller')
        self._load_servo_config()

        self.log.debug('Starting the multiprocessing pool')
        pool = Pool(processes=5)
        

    def set_stomp_client(self, client):
        """
        sets the stomp client for making call to the server to register for more move sequences
        @type client: StompClient
        @param client: the stomp client for sending messages to the server 
        """
        self.stompclient = client
    
    def _load_servo_config(self):
        """
            load the servo configuration files
            servomap contains the mapping from leg, and servo to servo channel
            servocalibration contains the fine parameters for centering and controlling range of servo movement
        """
        self.log.debug('Loading servo map data')
        json_data = open('config/servomap.json')
        self.servomap = json.load(json_data)
        json_data.close()
        self.log.info('Loaded config/servomap.json')

        self.log.debug('Loading servo calibration data')
        json_data = open('config/servocalibration.json')
        self.servocalibration = json.load(json_data)
        json_data.close()
        self.log.info('Loaded condig/servocalibration.json')

