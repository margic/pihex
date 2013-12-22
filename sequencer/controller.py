from multiprocessing import Queue
import util

__author__ = 'Paul'

""" Controls the sequencing of firing of leg movement based in provided sequence
    that is obtained from the rules system
    A reference to the controller queue is passed to each processor for to
    provide callback functionality to kick of next leg movement and allow for
    variances in leg timing to move each leg.
"""
__callbackQ = Queue()
logger = util.logger


def notify_movement_complete(movement):
    __callbackQ.put(movement)
    logger.debug('Movement complete queued' + movement)

