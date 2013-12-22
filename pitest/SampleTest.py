import util
import unittest

__author__ = 'Paul'
logger = util.logger


class TestSequence(unittest.TestCase):

    def setUp(self):
        logger.info('Set up TestSequence Tests')

    def testExample(self):
        logger.info('Test example method')
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()