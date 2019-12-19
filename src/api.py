"""
This is the test module and supports all the ReST actions for the
'test' collection
"""

# 3rd party modules
import pkg_resources
from flask import make_response, send_file
# native modules
import logging
import datetime
import platform
import socket
import git
import time
import json
import os
# local modules
from tsuro.tsurobot import Tsurobot, play_game

logger = logging.getLogger(__name__)
logger.info("logging from api: {0}".format(__name__))
config_file = "./config.json"
tsurobot = Tsurobot(config_file)


# TODO - remove commented functions from api.yml
def get_info():
    """
    This function responds to a request for /info
    with a lists of application and system info

    : return:        json with a 'packages' array and 'other' string
    """

    packages_list = [d.project_name + "==" +
                     pkg_resources.get_distribution(d.project_name).version
                     for d in pkg_resources.working_set]

    with open(config_file) as f:
        config = json.load(f)
    other = socket.gethostname() + " - " + platform.platform()

    return {'packages': packages_list, 'other': other, 'config': config}


def get_ack():
    """
    This function responds to a request for /ack
    with a lists of application and system info
    """

    return make_response('Tsuro ACK', 200)


def post_test_led(led, red, green, blue):
    "cycle through colors for each LED"
    response_message = "LED test success."
    return make_response(response_message, 200)


def post_led(led, red, green, blue):
    "change led color LED"
    tsurobot.light.set_led(led, red, green, blue)
    response_message = "led {0} color set to red={1}, green={2}, blue={3}".format(led, red, green, blue)
    return make_response(response_message, 200)


def get_front_ir():
    "get front IR sensor signals"
    signal = tsurobot.front_ir.get_front_ir()
    logger.info("IR signal: {0}".format(str(signal)))
    return signal


def get_button():
    "wait for and report a button press"
    press = tsurobot.button.await_input()
    return press


def post_beep(seconds):
    "sound buzzer for {0} seconds".format(seconds)
    tsurobot.sound.beep(seconds)
    response_message = "buzzer sounded for {0} seconds".format(seconds)
    return make_response(response_message, 200)


def get_bottom_ir():
    "get signal for bottom IR sensors"
    # TODO
    signal = tsurobot.bottom_ir.get_analog_read()
    return signal


def get_receiver_ir():
    "get key from IR receiver"
    # TODO
    key = tsurobot.receiver_ir.await_key()
    logger.info(str(key))
    return key


def put_git_pull(branch_name):
    """
    This function responds to a request for /git and
    updates the Tsurobot with the latest from the given branch
    """
    # git pull origin [branch]
    g = git.Git('./')
    g.pull('origin', branch_name)
    repo = git.Repo('./')
    branch = repo.head.ref.name
    commit_id = str(repo.head.commit)
    commit_message = repo.head.commit.message
    response_message = 'Successful git pull on {0} for commit {1}: {2}'.format(branch, commit_id, commit_message)
    logging.info(response_message)

    return make_response(response_message, 200)


def post_test_wheels():
    """
    This function responds to a request for /test_wheels/
    with a '200' upon successful startup
    """
    # TODO - adapt to alphabot
    tsurobot.steering.test()

    return make_response('Tsurobot wheel test complete', 200)


def post_test_vertical_view():
    """
    This function responds to a request for /test_vertical_view/
    with a '200' upon success
    """
    # TODO - adapt to alphabot
    logger.info("tilt to 0")
    tsurobot.camera.servos.tilt_absolute(0)
    time.sleep(1)
    logger.info("tilt to 100")
    tsurobot.camera.servos.tilt_absolute(100)
    time.sleep(1)
    logger.info("tilt to 0")
    tsurobot.camera.servos.tilt_absolute(0)
    time.sleep(1)
    logger.info("tilt to -100")
    tsurobot.camera.servos.tilt_absolute(-100)
    time.sleep(1)
    logger.info("tilt to 0")
    tsurobot.camera.servos.tilt_absolute(0)
    time.sleep(1)
    return make_response('Tsurobot vertical view test complete', 200)


def post_look_at(pan, tilt):
    """
    This function responds to a request for /look_at/
    with a '200' upon success
    """
    # TODO - adapt to alphabot
    tsurobot.camera.servos.tilt_absolute(tilt)
    tsurobot.camera.servos.pan_absolute(pan)
    return make_response('Tsurobot is looking at target [{0}, {1}]'.format(pan, tilt), 200)


def post_calibrate_pan(offset):
    """
    This function responds to a request for /calibrate_pan/
    with a '200' upon success
    """
    # TODO - adapt to alphabot
    tsurobot.camera.calibrate_pan(pan=offset)
    tsurobot.camera.save_calibration()
    return make_response('Tsurobot pan is offset to {0}'.format(tsurobot.camera.config["pan_offset"]), 200)


def post_calibrate_tilt(offset):
    """
    This function responds to a request for /calibrate_pan/
    with a '200' upon success
    """
    # TODO - adapt to alphabot
    tsurobot.camera.calibrate_tilt(tilt=offset)
    tsurobot.camera.save_calibration()
    return make_response('Tsurobot tilt is offset to {0}'.format(tsurobot.camera.config["tilt_offset"]), 200)


def post_test_horizontal_view():
    """
    This function responds to a request for /test_horizontal_view/
    with a '200' upon success
    """
    # TODO - adapt to alphabot
    logger.info("pan to 0")
    tsurobot.camera.servos.pan_absolute(0)
    time.sleep(1)
    logger.info("pan to -100")
    tsurobot.camera.servos.pan_absolute(-100)
    time.sleep(1)
    logger.info("pan to 0")
    tsurobot.camera.servos.pan_absolute(0)
    time.sleep(1)
    logger.info("pan to 100")
    tsurobot.camera.servos.pan_absolute(100)
    time.sleep(1)
    logger.info("pan to 0")
    tsurobot.camera.servos.pan_absolute(0)
    time.sleep(1)
    return make_response('Tsurobot horizontal view test complete', 200)


def post_camera_still():
    """
    This function responds to a request for /test_front_wheels/
    with a '200' upon successful startup
    """
    file_path = ".././temp/capture.jpg"
    tsurobot.camera.vision.grab_still()
    new_name = "capture_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    os.rename(file_path, ".././temp/" + new_name + ".jpg")

    return make_response('Tsurobot still grabbed.', 200)


def get_camera_still():
    """
    This function responds to a request for /test_front_wheels/
    with a '200' upon successful startup
    """
    file_name = ".././temp/capture.jpg"
    tsurobot.camera.vision.grab_still()
    try:
        return send_file(file_name, mimetype='image/jpeg')
    finally:
        os.remove(file_name)


def post_camera_burst():
    """
    This function responds to a request for /get_camera_burst/
    with a list of photos upon successful capture of a burst of photos
    """
    logging.info(f"start: {datetime.datetime.now()}")
    for i in range(60):
        tsurobot.camera.vision.grab_still_mem()
        logging.info(f"capture {i}: {datetime.datetime.now()}")
    logging.info(f"end: {datetime.datetime.now()}")
    return make_response('Burst finished', 200)


def post_play_game(action):
    """
    This function responds to a request for /tsuro/launch_game
    with a '200' upon successful completion
    """
    play_game(tsurobot)
    return make_response('Tsuro game play complete', 200)
