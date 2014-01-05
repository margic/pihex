from logging import FileHandler

__author__ = 'Paul'
import logging
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger(__name__)
#hdl = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = TimedRotatingFileHandler('/var/log/pihex/pihex.log', when='H', interval=24)
file_handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
#logger.addHandler(hdl)
logger.addHandler(file_handler)