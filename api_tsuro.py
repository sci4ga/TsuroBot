"""
This is the tsuro module and supports all the ReST actions for the
'tsuro' collection
"""
# import 3rd party modules
from flask import make_response


def post_launch_game():
    """
    This function responds to a request for /tsuro/launch_game
    with a '200' upon successful completion
    """
    from tsuro import tsurobot

    tsurobot.launch_game()

    return make_response('Tsuro game play complete', 200)
