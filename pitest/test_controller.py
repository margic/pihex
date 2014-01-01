from unittest import TestCase
from sequencer.controller import Controller

__author__ = 'paul'


class TestController(TestCase):
    def setUp(self):
        super(TestController, self).setUp()
        self.controller = Controller()
        move = dict()
        move['leg'] = 1
        move['servo'] = 'femur'
        move['angle'] = 10
        move['duration'] = 100
        self.move = move

    def test_process_move(self):
        servo_instruction = self.controller.process_move(self.move)
        expected = {'duration': 100, 'current_pulse': 307, 'new_pulse': 324, 'channel': 4}
        self.assertDictEqual(expected, servo_instruction, 'wrong move calculated')
        print servo_instruction

    def test_get_channel_from_move(self):
        # move looks like         "leg": 1,"servo": "femur","angle": 10,"duration": 1000
        channel = self.controller.get_channel_from_move(self.move)
        self.assertEquals(4, channel, 'returned wrong channel')

    def test_get_current_pulse_by_channel(self):
        pulse = self.controller.get_current_pulse_by_channel(0)
        self.assertEquals(307, pulse, 'did not return default current pulse')

    def test_get_calib_by_channel(self):
        calib = self.controller.get_calib_by_channel(0)
        expected = dict()
        # "channel": 0
        # "center": 307
        # "min": 205
        # "max": 409
        expected['channel'] = 0
        expected['center'] = 307
        expected['min'] = 205
        expected['max'] = 409
        self.assertDictEqual(expected, calib, 'wrong calibration')

    def test_get_center_by_channel(self):
        center = self.controller.get_center_by_channel(0)
        self.assertEquals(307, center, 'wrong center')

    def test_get_pulse_per_degree(self):
        pulse_degree = self.controller.get_pulse_per_degree()
        self.assertEquals(1.7, pulse_degree, 'wrong pulse per degree')