# standard imports
import time
# local imports
from system import initcheck, syscheck
from sensors import buttonpress, envcheck
from actions import calibrate, followpath, approachboard, identifytile, stopeverything


state = "Initialize"
while(True):
    if state == "Initialize":
        # LED: solid red
        state = initcheck()
    elif state == "AwaitPrelaunch":
        # LED: blinking red
        if buttonpress():
            state = "SystemsCheck"
    elif state == "SystemsCheck":
        # LED: solid yellow
        state = syscheck()
    elif state == "EnvironmentCheck":
        # LED: blinking yellow
        state = envcheck()
    elif state == "Calibrate":
        # LED: solid green
         state = calibrate()
    elif state == "AwaitLaunch":
        # LED: blinking green
        if buttonpress():
            state = "Launch"
    elif state == "Launch":
        # LED: off
        # SOUND: roar
        state = approachboard()
    elif state == "AwaitTile":
        # SOUND: stationary dragon
        state = identifytile()        
    elif state == "FollowPath":
        # SOUND: moving dragon
        state = followpath()
    elif state == "Collision":
        # SOUND: chicken
        if buttonpress():
            state = "AwaitPrelaunch"
    elif state == "ExitPath":
        # SOUND: sad trombone
        if buttonpress():
            state = "AwaitPrelaunch"
    else:
        stopeverything()
        raise ValueError("State '" + str(state) + "' isn't valid.")
