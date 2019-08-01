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

with open('config.json') as f:
    config = json.load(f)
# Configure log level available to handlers
logging.basicConfig(level=logging.DEBUG)
# Configure log handler output directory, rotation, output format
handler = TimedRotatingFileHandler(config["log_file"], when=config["log_rotation"], backupCount=config["log_backups"])
handler.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s:%(message)s'))
# Configure log level for file output of log handler
if config['debug_state']:
    handler.setLevel(logging.DEBUG)
else:
    handler.setLevel(logging.INFO)
logging.getLogger('').addHandler(handler)
logger = logging.getLogger(__name__)

app = connexion.App(__name__, specification_dir='./')
app.add_api(config["api_yml"])


@app.route('/')
def index():
    # TODO: supply list of logs
    templateData = {'logs': []}
    return render_template(config["template"], **templateData)


if __name__ == "__main__":
    app.run(host=config["host"], port=config["port"], debug=config["debug_state"])
