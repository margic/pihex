import time
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
        self.log = util.logger
        self._load_servo_config()
        self.previous_position = list()
        for x in range(0, 18, 1):
            self.previous_position.append(0)

    def start(self):
        """
            starts the controller and prepares it for receiving sequences
        """
        self.log.info('Initializing the controller')
        pool = Pool(processes=5)
    
    def _load_servo_config(self):
        """
            load the servo configuration files
            servomap contains the mapping from leg, and servo to servo channel
            servocalibration contains the fine parameters for centering and controlling range of servo movement
        """
        self.log.debug('Loading servo map data')
        json_data = open('servomap.json')
        self.servomap = json.load(json_data)
        json_data.close()
        self.log.info('Loaded servomap.json')

        self.log.debug('Loading servo calibration data')
        json_data = open('servocalibration.json')
        self.servocalibration = json.load(json_data)
        json_data.close()
        self.log.info('Loaded servocalibration.json')

    def process_sequence(self, sequence):
        """
        @param sequence: the movement sequence to execute
        @return: dictionary of sensor readings
        """
        self.log.debug('process sequence')
        # parse the json message
        jseq = json.loads(sequence)
        moveseq = jseq['sequence']

        for moves in moveseq:
            self.log.debug('processing move %s' % moves)
            for move in moves:
                self.process_move(move)

    def process_move(self, move):
        self.log.debug('processing step %s' % move)
        # start a process from the pool to process each step in this move in the sequence
        # resolve channel
        servo = move['servo']
        legnum = move['leg']
        map = self.servomap['servoMap']
        leg = map[legnum]
        channel = leg[servo]

        calibmap = self.servocalibration['servoCalibration']
        pulsedeg = float(self.servocalibration['pulsePerDegree'])
        calib = calibmap[channel]
        # add the previous position to the calibration dict
        calib['prevposdeg'] = self.previous_position[channel]
        # got all the move params start moving servo in a process
        move_servo(prev_pos, move['position'], move['speed'], channel)


def move_servo(prev_pos, new_pos, speed, channel):
    sleeptime = 50
    delta = abs(prev_pos - new_pos)
    step = delta / float(speed) / float(sleeptime)

    position = step

    for x in range(0, speed, sleeptime):
        print('position %d' % position)
        time.sleep(50 / float(1000))