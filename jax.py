from sequencer import controller
import util
from multiprocessing import Pool

__author__ = 'Paul'

""" This is the main start point for the JAX robot
    This starts the client and control system
"""
logger = util.logger
callback = controller.notify_movement_complete


def hello(greeting):
    print(greeting)
    return 'x'


def main():
    logger.info('Starting the JAX robot controller')
    logger.info('Initializing motion worker pool')
    pool = Pool(10)
    pool.apply_async(hello, args=('hello',), callback=callback)
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()