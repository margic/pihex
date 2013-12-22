__author__ = 'Paul'
import logging


logger = logging.getLogger(__name__)
hdl = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
logger.addHandler(hdl)