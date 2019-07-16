# import native modules
import time
# local imports
import picar


class Tsurobot:
    def __init__(self, db_file):
        self.front_wheels = picar.front_wheels.Front_Wheels(debug=False, db=db_file)
        self.back_wheels = picar.back_wheels.Back_Wheels(debug=False, db=db_file)
        self.front_wheels.ready()
        self.back_wheels.ready()
        self.next_game_action = "look_for_board"

    def test_back_wheels(self):
        self.back_wheels.speed = 50
        self.back_wheels.forward()
        time.sleep(2)
        self.back_wheels.stop()
        time.sleep(1)
        self.back_wheels.backward()
        time.sleep(2)
        self.back_wheels.stop()

    def test_front_wheels(self):
        self.front_wheels.turn_left()
        time.sleep(1)
        self.front_wheels.turn_straight()
        time.sleep(1)
        self.front_wheels.turn_right()
        time.sleep(1)
        self.front_wheels.turn_straight()

    def launch_game(self):
        while(self.game_state != "DONE"):
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


picar.setup()
tsurobot = Tsurobot("./config")
