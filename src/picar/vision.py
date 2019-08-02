import json
import logging

logger = logging.getLogger(__name__)

class Vision(object):

    def __init__(self, config_file='./config_vision.json'):
        ''' Init camera vision '''
        logger.info("Initializing Camera vision with config: {0}".format(str(config_file)))
        with open(config_file) as f:
            self.config = json.load(f)

    def save_config(self):
        with open(self.config["config_file"], 'w') as outfile:
            json.dump(self.config, outfile)
