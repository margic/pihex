from logging import FileHandler

__author__ = 'Paul'
import logging
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger(__name__)
#hdl = logging.StreamHandler()
file_handler = FileHandler('/var/log/pihex/pihex.log')
logger.setLevel(logging.DEBUG)
#logger.addHandler(hdl)
logger.addHandler(file_handler)