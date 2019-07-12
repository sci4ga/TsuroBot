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

    import picar
    from picar import back_wheels, front_wheels

    picar.setup()
    db_file = "/Users/andrewtsai/personal-projects/RobotTsuro/config"
    fw = front_wheels.Front_Wheels(debug=False, db=db_file)
    bw = back_wheels.Back_Wheels(debug=False, db=db_file)
    bw.ready()
    fw.ready()

    SPEED = 60
    bw_status = 0
    bw.speed = SPEED
    bw.forward()
    bw_status = 1
    import os
    os.cmd('python3 ./tsuro/start.py')
    
    return make_response('Tsuro started: speed' + SPEED, 200)

def get_stop():
    """
    This function responds to a request for /tsuro/stop
    with a '200' upon successful stop
    """
    import picar
    from picar import back_wheels, front_wheels

    picar.setup()
    db_file = "/Users/andrewtsai/personal-projects/RobotTsuro/config"
    fw = front_wheels.Front_Wheels(debug=False, db=db_file)
    bw = back_wheels.Back_Wheels(debug=False, db=db_file)
    bw.ready()
    fw.ready()

    SPEED = 60
    bw_status = 0
    bw.stop()
    bw_status = 0

    return make_response('Tsuro stop', 200)
