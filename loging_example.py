#!/usr/bin/env python
# coding=utf-8
"""
Simple example of loging
src: http://www.slideshare.net/MinskPythonMeetup/ss-32114024#
"""

import sys
import logging

# inicialize
logging.basicConfig(
    format='%(asctime)s  %(name)s [%(levelname)s] %(message)s',
    stream=sys.stdout,
    level=logging.INFO)

# first word of script. Horay!
logger = logging.getLogger('example.frizzy')
logger.info("i'm alive!")

# levels
logger.critical('50: problem, after which the application can not recover unaided')
logger.error('40: an issue where the application is not working in normal mode')
logger.warning('30: problem that does not interfere with the application, but which is worth paying attention')
logger.info('20: regular entry in the log')
logger.debug('10: logs that are required for debugging and hardly useful further')

#
logger.warning('Warning with traceback', exc_info=True)

#
logger.info('%s %s', 'lazy', 'formatting')

# no space left on device
from logging.handlers import *
RotatingFileHandler(
    filename, mode='a',
    maxBytes=0, backupCount=0,
    encoding=None, delay=False)

TimeRotatingFileHandler(
    filename, 
    when='h', interval=1,
    backupCount=0, encoding=None,
    delay=False, utc=False)