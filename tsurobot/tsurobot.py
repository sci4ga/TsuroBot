# local imports
from picar import picarv

'''
we want a state machine
each state "function" should only have logic for what happens in that state
    granularity goes down to "move this motor"
    returns success or failure, and nothing else
        maybe details of success or failure, but it shouldn't care about how that success or failure gets handled
Something else (say, def state_machine?) determines how to move from one state to the other
    and what to do when something fails or succeeds
'''

class Tsurobot(picarv.PicarV):
    def __init__(self, db_file):
        self.next_game_action = "look_for_board"
        self.location = None
        picarv.PicarV.__init__(self, db_file)

    def launch_game(self, action="state_look_for_board"):
        self.next_game_action = action
        while(self.next_game_action):
            self.next_game_action = getattr(self, self.next_game_action)()
        return None

    def state_look_for_board(self):
        '''
        This checks if the robot is in the start position of the board.
        It returns the appropriate next state as a string.
        '''
        # note: car will be in a calibration box that's in front of the edge of the board
        # Maybe rename to something that means "Verify I am in calibration box"?
        # camera check and calibrate by looking up and down for start dot / pair of dots that have directionality
        # beep happily
        self.camera.tilt_down_max()
        self.update_location()
        if self.location == "CALIBRATION BOX":
            '''
            need to think about if openCV is async or not. If so camera object will just update the location and we can just check it
            If not, we need to call a function to get the location.
            '''
            return "state_calibrate_to_board"
        else:
            return "state_look_for_board"

    def state_calibrate_to_board(self):
        '''
        This directs the robot to calibrate sensors relative to the start position.
        It returns the appropriate next state as a string.
        '''
        # note: car will be in a calibration box that's in front of the edge of the board
        # camera white balance
        # camera pan and tilt so that it can look for next path
        # make sure front wheels are straight
        # check which direction is forward and backward for back wheels
        # TODO: use a method here to calibrate
        if self.calibrate():
            return "state_move_to_start"
        else:
            return None

    def state_move_to_start(self):
        '''
        This directs the robot to move from start position to the edge of the tile area.
        It returns the appropriate next state as a string.
        '''
        # move forward until we see start mark
        raise NotImplementedError
        while self.camera.location != "START"
        next_action = "await_tile"
        return next_action

    def state_await_tile(self):
        '''
        This directs the robot to look for a tile played in the immediate tile area.
        It returns the appropriate next state as a string.
        '''
        # Camera looks at path
        # Once cv says "path exists" and "tile is completely set down", move to follow_path
        raise NotImplementedError
        next_action = "follow_path"
        return next_action

    def state_follow_path(self):
        '''
        This directs the robot to folow the path until a stop condition is reached.
        It returns the appropriate next state as a string.
        '''
        # follow the path using CV (be able to correct steering for small errors, but not overcorrect)
        # once CV says "edge of board imminent", move to await_tile
        # if you see bot, move to DONE and make sad noise
        # If you see edge / start position again, move to DONE and make sad noise
        raise NotImplementedError
        next_action = "await_tile"
        return next_action

def stateMachine():
