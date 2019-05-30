# standard imports
import time
# local imports
from system import initcheck, syscheck
from sensors import buttonpress, envcheck
from actions import calibrate, followpath, approachboard, identifytile


state = "Initialize"
while(True):
    if state == "Initialize":
        state = initcheck()
    elif state == "AwaitPrelaunch":
        if buttonpress():
            state = "SystemsCheck"
    elif state == "SystemsCheck":
        state = syscheck()
    elif state == "EnvironmentCheck":
        state = envcheck()
    elif state == "Calibrate":
         state = calibrate()
    elif state == "AwaitLaunch":
        if buttonpress():
            state = "Launch"
    elif state == "Launch":
        state = approachboard()
    elif state == "AwaitTile":
        state = identifytile()        
    elif state == "FollowPath":
        state = followpath()
    elif state == "Collision":
        if buttonpress():
            state = "AwaitPrelaunch"
    elif state == "ExitPath":
        if buttonpress():
            state = "AwaitPrelaunch"
    else:
        raise ValueError("State '" + str(state) + "' isn't valid.")
