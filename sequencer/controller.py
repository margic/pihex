import ConfigParser
from threading import Thread, Condition
import time
from sequencer.ada_pwm import AdaPwm
from sequencer.mock_pwm import MockPwm
from client.stompclient import StompClient
import util
import json
from Queue import Queue

__author__ = 'Paul'

#   Controls the sequencing of firing of leg movement based in provided sequence
#   that is obtained from the rules system


class Controller():
    def __init__(self):
        """
        @type queue_config: dict
        @param queue_config: the message queue configuration
        @return:
        """
        # load config properties
        config = ConfigParser.ConfigParser()
        config.read('config/settings.cfg')
        self.queue_config = dict()
        self.queue_config['remote_queue_host'] = config.get('RemoteQueue', 'host')
        self.queue_config['remote_queue_port'] = config.getint('RemoteQueue', 'port')
        self.queue_config['remote_queue_username'] = config.get('RemoteQueue', 'username')
        self.queue_config['remote_queue_password'] = config.get('RemoteQueue', 'password')
        self.remote_receive_queue = config.get('RemoteQueue', 'receive_queue')
        self.remote_send_queue = config.get('RemoteQueue', 'send_queue')
        self.started = False
        self.servo_map = None
        self.servo_calibration = None
        self.log = util.logger
        self._load_servo_config()
        self.current_pulse = list()
        self.pwm_queue = Queue()
        self.pwm_sender = MockPwm()
        self.pwm_thread = None
        self.stomp = None
        # set up default servo centers
        for x in range(0, 18, 1):
            self.current_pulse.append(self.get_center_by_channel(x))

    def set_pwm_sender(self, sender):
        self.pwm_sender = sender

    def stop(self):
        self.started = False
        self.stomp.stop_client()
        self.pwm_thread.stop()

    def start(self):
        """
            starts the controller and prepares it for receiving sequences
        """
        self.log.info('Initializing the controller')
        self.set_pwm_sender(AdaPwm())
        self.started = True
        self.log.info('Starting the pwm queue thread')
        self.pwm_thread = PwmThread(self.pwm_queue, self.pwm_sender)
        self.pwm_thread.setName('Pwm Dequeue Thread')
        self.pwm_thread.setDaemon(False)
        self.pwm_thread.start()

        # start the stomp client
        remote_receive_queue = self.remote_receive_queue
        remote_send_queue = self.remote_send_queue

        stomp_client = StompClient(self.queue_config)
        stomp_client.set_controller(self)
        stomp_client.start_listener(remote_receive_queue)

        stomp_client.send_signon(remote_send_queue)
        self.stomp = stomp_client
        while bool(self.started):
            time.sleep(2)

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
            condition = Condition()
            thread_count = 0
            for move in moves:
                thread_count += 1
                servo_instruction = self.process_move(move)
                move_servo_thread = ServoThread(servo_instruction, self.pwm_queue, condition, thread_count, self.update_current_pulse)
                move_servo_thread.setDaemon(False)
                move_servo_thread.setName('Servo %d' % servo_instruction['channel'])
                move_servo_thread.start()
            condition.acquire()
            if thread_count > 0:
                condition.wait()
            # wait for all threads to finish before doing next loop
            condition.release()

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

    def update_current_pulse(self, new_pulse):
        """
        @type updated_value: tuple
        @param updated_value:
        @return:
        """
        self.log.debug(new_pulse)
        channel = new_pulse[0]
        value = new_pulse[1]
        self.current_pulse[channel] = value


class PwmThread(Thread):
    def __init__(self, pwm_queue, pwm_sender):
        """
        @type pwm_queue: Queue
        @type pwm_sender: PwmSender
        @param pwm_queue:
        @param pwm_sender: the sender that sends the pulse items
        @return:
        """
        Thread.__init__(self)
        self.pwm_queue = pwm_queue
        self.pwm = pwm_sender
        self.log = util.logger
        self.started = False

    def run(self):
        self.started = True
        while self.started:
            pwm_item = self.pwm_queue.get(block=True)
            self.log.debug('Dequeue pwm item %s' % (pwm_item,))
            if repr(pwm_item) == 'Terminate':
                self.log.info("Terminate message on pwm queue")
            else:
                self.pwm.set_servo_pulse(pwm_item)

    def stop(self):
        self.started = False
        self.pwm_queue.put('Terminate')


class ServoThread(Thread):

    def __init__(self, servo_instruction, pwm_queue, condition, thread_count, update_current_pulse):
        """
        @type servo_instruction: dict
        @type pwm_queue: Queue
        @param servo_instruction:
        @param pwm_queue:
        @return:
        """
        Thread.__init__(self)
        self.servo_instruction = servo_instruction
        self.log = util.logger
        self.pwm_queue = pwm_queue
        self.condition = condition
        self.thread_count = thread_count
        self.update_current_pulse = update_current_pulse

    def run(self):
        self.log.debug('starting servo thread')
        self.move_servo(self.servo_instruction)
        self.condition.acquire()
        self.thread_count -= 1
        self.condition.notify()
        self.condition.release()

    def move_servo(self, servo_instruction):
        """
        @todo add code to ensure values do not exceed servo max and min
        @param servo_instruction:
        @return:
        """
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
                self.log.debug('servo channel %s pulse %d' % (channel, step_pulse))
                pwm_item = channel, 0, step_pulse
                self.pwm_queue.put(pwm_item)
                time.sleep(sleep_time/1000)
            self.log.debug('servo channel %s pulse %d' % (channel, new_pulse))
            pwm_item = channel, 0, new_pulse
            self.pwm_queue.put(pwm_item)
            update_pulse = channel, new_pulse
            self.update_current_pulse(update_pulse)