import util
import json
__author__ = 'Paul'

#   Controls the sequencing of firing of leg movement based in provided sequence
#   that is obtained from the rules system


class Controller():
    def __init__(self):
        servomap = None
        servcalibration = None
        self.log = util.logger

    def start(self):
        """
            starts the controller and prepares it for receiving sequences
        """
        self._load_servo_config()
        self.log.info('Initializing the controller')

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

