"""
This is the test module and supports all the ReST actions for the
'test' collection
"""

# 3rd party modules
import pkg_resources
from flask import make_response
# native modules
import logging
import platform
import socket
import git
# local modules


def get_info():
    """
    This function responds to a request for /test/info
    with a lists of application and system info

    : return:        json with a 'packages' array and 'other' string
    """

    packages_list = [d.project_name + "==" + pkg_resources.get_distribution(d.project_name).version
                     for d in pkg_resources.working_set]
 
    other = socket.gethostname() + " - " + platform.platform()

    return {'packages': packages_list, 'other': other}


def get_test():
    """
    This function responds to a request for /test/info
    with a lists of application and system info
    """

    return make_response('Test successful', 200)

def git_pull():
    """
    This function updates the RobotTsuro code in the raspberry pi without the need for ssh
    """
    g = git.cmd.Git(git_dir)
    g.pull()



