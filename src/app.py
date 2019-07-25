"""
Starts logging and the PicarTsuro app w/ API via connexion
"""
# 3rd party modules
import connexion
from flask import render_template
# native modules
import json
import logging
from logging.handlers import TimedRotatingFileHandler

# Configure logger directory and rotation, output format, and level
logfile = ".././logs/tsuro.log"
logging.basicConfig(level=logging.DEBUG)
handler = TimedRotatingFileHandler(logfile, when="midnight", backupCount=30)
handler.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s:%(message)s'))
handler.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(handler)
logger = logging.getLogger(__name__)

with open('config.json') as f:
    envconfig = json.load(f)
if not envconfig['debug_enabled']:
    logger.setLevel(logging.INFO)

app = connexion.App(__name__, specification_dir='./')
app.add_api('api.yml')


@app.route('/')
def index():
    # TODO: supply list of logs
    templateData = {'logs': []}
    return render_template('index.html', **templateData)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4800, debug=True)
