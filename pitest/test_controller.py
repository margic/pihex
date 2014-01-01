from unittest import TestCase
from sequencer.controller import Controller

__author__ = 'paul'


class TestController(TestCase):

    def setUp(self):
        self.controller = Controller()

    def test__load_servo_config(self):
        self.assertTrue(True)

    def test_process_sequence(self):
        test_sequence_file = open('testsequence.json')
        test_sequence = test_sequence_file.read()
        test_sequence_file.close()
        self.controller.process_sequence(test_sequence)