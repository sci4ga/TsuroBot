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
# import git
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


def get_git_pull(branch_name):
    """
    This function updates the RobotTsuro code in the raspberry pi without the need for ssh
    """
    # git pull origin [branch]
    g = git.Git('./')
    g.pull('origin', branch_name)
    repo = git.Repo('./')
    branch = repo.head.ref.name
    commit_id = str(repo.head.commit)
    commit_message = repo.head.commit.message
    response_message = f'Successful git pull on {branch} for commit {commit_id}: {commit_message}'
    logging.info(response_message)

    return make_response(response_message, 200)
