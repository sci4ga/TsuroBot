# local imports
from picar import picarv


class Tsurobot(picarv.PicarV):
    def __init__(self, db_file):
        self.next_game_action = "look_for_board"
        picarv.PicarV.__init__(self, db_file)

    def launch_game(self):
        while(self.next_game_action != "DONE"):
            self.next_game_action = getattr(self, self.next_game_action)()
        return None

    def look_for_board(self):
        '''
        This checks if the robot is in the start position of the board.
        It returns the appropriate next state as a string.
        '''
        raise NotImplementedError
        next_action = ""
        return next_action

    def calibrate_to_board(self):
        '''
        This directs the robot to calibrate sensors relative to the start position.
        It returns the appropriate next state as a string.
        '''
        raise NotImplementedError
        next_action = ""
        return next_action

    def move_to_start(self):
        '''
        This directs the robot to move from start position to the edge of the tile area.
        It returns the appropriate next state as a string.
        '''
        raise NotImplementedError
        next_action = ""
        return next_action

    def await_tile(self):
        '''
        This directs the robot to look for a tile played in the immediate tile area.
        It returns the appropriate next state as a string.
        '''
        raise NotImplementedError
        next_action = ""
        return next_action

    def follow_path(self):
        '''
        This directs the robot to folow the path until a stop condition is reached.
        It returns the appropriate next state as a string.
        '''
        raise NotImplementedError
        next_action = ""
        return next_action
