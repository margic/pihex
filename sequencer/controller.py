from multiprocessing import Queue, Pool
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
pool = Pool(10)


def hello(greeting):
    print(greeting)
    return 'x'


def init():
    logger.info('Initializing the controller')
    logger.debug('Initializing motion worker pool')
    pool.apply_async(hello, args=('hello',), callback=notify_movement_complete)
    pool.close()
    pool.join()


def notify_movement_complete(movement):
    __callbackQ.put(movement)
    logger.debug('Movement complete queued' + movement)

