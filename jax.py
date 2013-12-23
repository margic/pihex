from sequencer import controller
import util

__author__ = 'Paul'

""" This is the main start point for the JAX robot
    This starts the client and control system
"""
logger = util.logger


def main():
    logger.info('Starting the JAX robot controller')
    controller.init()

if __name__ == "__main__":
    main()