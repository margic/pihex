import time
import util
import json
from multiprocessing import Pool

__author__ = 'Paul'

#   Controls the sequencing of firing of leg movement based in provided sequence
#   that is obtained from the rules system


class Controller():
    def __init__(self):
        self.servo_map = None
        self.servo_calibration = None
        self.log = util.logger
        self._load_servo_config()
        self.current_pulse = list()
        for x in range(0, 18, 1):
            self.current_pulse.append(self.get_center_by_channel(x))

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
        self.servo_map = json.load(json_data)
        json_data.close()
        self.log.info('Loaded servomap.json')

        self.log.debug('Loading servo calibration data')
        json_data = open('servocalibration.json')
        self.servo_calibration = json.load(json_data)
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
                servo_instruction = self.process_move(move)
                move_servo(servo_instruction)

    def process_move(self, move):
        """
        Processes the incoming move from the sequence and creates a servo instruction set to send
        to the process that makes the servo move. Resolves name and angle to channel and pulse settings
        @param move: incoming dict containing the move from the sequence has servo name and angle
        @return: the servo instruction dict
        @type move: dict
        @rtype: dict
        """
        self.log.debug('processing step %s' % move)
        # resolve channel
        channel = self.get_channel_from_move(move)

        # get the servo calibration details for channel
        pulsedeg = self.get_pulse_per_degree()
        calib = self.get_calib_by_channel(channel)

        # calculate the end position
        current_pulse = self.get_current_pulse_by_channel(channel)
        center = self.get_center_by_channel(channel)
        new_pulse = int(center + (move['angle'] * pulsedeg))

        #prepare the move details in a dict
        servo_instruction = dict()
        servo_instruction['channel'] = channel
        servo_instruction['duration'] = move['duration']
        servo_instruction['current_pulse'] = current_pulse
        servo_instruction['new_pulse'] = new_pulse
        return servo_instruction

    def get_channel_from_move(self, move):
        """
        returns the channel name specified in a move from the sequence of moves
        supplied
        @type move: dict
        @rtype: int
        @param move: incoming move info from sequence
        @return: channel number for corresponding servo
        """
        servo_name = move['servo']
        leg_number = move['leg']
        servo_map = self.servo_map['servoMap']
        leg = servo_map[leg_number]
        channel = leg[servo_name]
        return channel

    def get_current_pulse_by_channel(self, channel):
        """
        returns the current position of a servo channel in pulse length by channel
        @rtype: int
        @param channel: channel to look up current position
        @return: pulse length of current position
        """
        return self.current_pulse[channel]

    def get_calib_by_channel(self, channel):
        """
        returns the calibration dict for the specified servo channel
        includes the max, min and center calibration for servo
        @type channel: int
        @rtype: dict
        @param channel: channel number of servo
        @return: calibration dict for servo channel
        """
        calibmap = self.servo_calibration['servoCalibration']
        calib = calibmap[channel]
        return calib

    def get_center_by_channel(self, channel):
        """
        returns the center pulse length for a servo channel
        @param channel: the servo channel
        @type channel: int
        @rtype: int
        @return: the center pulse length for this channel
        """
        calib = self.get_calib_by_channel(channel)
        return calib['center']

    def get_pulse_per_degree(self):
        """
        returns the num pulse length that represents a single degree
        zero degrees represents servo center or pulse of 1.5ms pwm control translates that
        to approx 307 pulse end time. To move servo from center 0 degree to +1 degree add
        pulse per degree to center 307
        @return: pulse per degree
        @rtype: float
        """
        return float(self.servo_calibration['pulsePerDegree'])


def move_servo(servo_instruction):
    sleep_time = 50.0

    channel = servo_instruction['channel']
    duration = servo_instruction['duration']
    current_pulse = servo_instruction['current_pulse']
    new_pulse = servo_instruction['new_pulse']
    steps = duration / sleep_time
    # create a range object
    dif = (new_pulse - current_pulse) * 100
    step_float = dif / steps
    step = int(round(step_float))

    if step != 0:
        #building a range that needs int values multiply by 100 to increase resolution for servo movement
        for x in range(current_pulse * 100, new_pulse * 100, step):
            step_pulse = x / 100
            print 'servo channel %s pulse %d' % (channel, step_pulse)
            time.sleep(sleep_time/1000)
        print 'servo channel %s pulse %d' % (channel, new_pulse)