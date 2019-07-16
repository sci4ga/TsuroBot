"""
This is the tsuro module and supports all the ReST actions for the
'tsuro' collection
"""
# import 3rd party modules
from flask import make_response
# import native modules
import logging


def get_start():
    """
    This function responds to a request for /tsuro/start
    with a '200' upon successful startup
    """
    from tsuro import tsurobot

    tsurobot.back_wheels.speed = 50
    tsurobot.back_wheels.forward()

    return make_response('Tsuro started', 200)


def get_stop():
    """
    This function responds to a request for /tsuro/stop
    with a '200' upon successful stop
    """
    from tsuro import tsurobot

    tsurobot.back_wheels.stop()

    return make_response('Tsuro stop', 200)

def post_launch_game():
    """
    This function responds to a request for /tsuro/launch_game
    with a '200' upon successful completion
    """
    from tsuro import tsurobot

    tsurobot.launch_game()

    return make_response('Tsuro game complete', 200)