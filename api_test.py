"""
This is the test module and supports all the ReST actions for the
'test' collection
"""

# 3rd party modules
import pip
# local modules


def get_info():
    """
    This function responds to a request for /test/info
    with a lists of application and system info

    : return:        json with a 'packages' array and 'other' string
    """

    packages_list = sorted(["%s==%s" % (i.key, i.version) for i in pip.get_installed_distributions()])

    other = "in progress"

    return {'packages': packages_list, 'other': other}