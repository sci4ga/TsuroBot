import json
import logging

logger = logging.getLogger(__name__)

class Vision(object):
    '''Computer Vision / Camera vision class'''

    def __init__(self, config_file):
        ''' setup channels and basic stuff '''
        logger.info("Initializing front wheels with config_file: {0}".format(str(config_file)))
        with open(config_file) as f:
            self.config = json.load(f)