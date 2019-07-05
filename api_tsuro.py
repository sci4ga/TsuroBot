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

    return make_response('Tsuro started', 200)

def get_stop():
    """
    This function responds to a request for /tsuro/stop
    with a '200' upon successful stop
    """

    return make_response('Tsuro stop', 200)
