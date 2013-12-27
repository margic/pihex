from multiprocessing import Queue, Pool
import util

__author__ = 'Paul'


#   Controls the sequencing of firing of leg movement based in provided sequence
#   that is obtained from the rules system
#   A reference to the controller queue is passed to each processor for to
#   provide callback functionality to kick of next leg movement and allow for
#   variances in leg timing to move each leg.


_callbackQ = Queue()
logger = util.logger


def hello(greeting):
    print(greeting)
    return 'x'


def start():
    logger.info('Initializing the controller')
    logger.debug('Initializing motion worker pool')


def notify_movement_complete(movement):
    _callbackQ.put(movement)
    logger.debug('Movement complete queued' + movement)

