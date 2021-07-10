import logging
import os
logging.basicConfig(level=logging.INFO)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'