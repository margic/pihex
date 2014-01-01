__author__ = 'Paul'
import logging


logger = logging.getLogger(__name__)
stomplog = logging.getLogger('stomp.py')
hdl = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
stomplog.setLevel(logging.INFO)
logger.addHandler(hdl)
stomplog.addHandler(hdl)