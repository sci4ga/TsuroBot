# local imports
from picar import picarv
import logging

logger = logging.getLogger(__name__)


class Tsurobot(picarv.PicarV):
    """
    There ain't no bot like a Tsurobot.
    """
    def __init__(self, config_json="./config.json"):
        logger.info("Initializing Tsurobot with config: {0}".format(str(config_json)))
        picarv.PicarV.__init__(self, config_json)

    def look_for_board(self):
        """
        This checks if the Tsurobot is in the calibration position on the board.

        Returns:
            True if calibration area found, False otherwise
        """
        logger.info("Looking for board")
        # note: car will be in a calibration box that's in front of the edge of the board
        # Maybe rename to something that means "Verify I am in calibration box"?
        # camera check and calibrate by looking up and down for start dot / pair of dots that have directionality
        # beep happily
        raise NotImplementedError
        self.camera.tilt_down_max()
        self.update_location()
        if self.location == "CALIBRATION BOX":
            '''
            need to think about if openCV is async or not.
            If so camera object will just update the location and we can just check it
            If not, we need to call a function to get the location.
            '''
        return True

    def calibrate_to_board(self):
        '''
        This calibrates the camera whitebalance, pan positions, tilt postions,
        front wheel position, and rear wheel configuration of the Tsurobot.

        Returns:
            True if calibration succeeds, False otherwise
        '''
        logger.info("Calibrating to board")
        # note: car will be in a calibration box that's in front of the edge of the board
        # camera white balance
        # camera pan and tilt so that it can look for next path
        # make sure front wheels are straight
        # check which direction is forward and backward for back wheels
        # TODO: use a method here to calibrate
        raise NotImplementedError
        return True

    def move_to_start(self):
        '''
        This moves the Tsurobot from calibration area to the board edge/start position.

        Returns:
            True if successful, False otherwise
        '''
        logger.info("Moving to start")
        # move forward until we see start mark
        raise NotImplementedError
        return True

    def await_tile(self):
        '''
        This looks for a Tsuro tile played in the tile area immediately in front of the Tsurobot.

        Returns:
            True if a Tsuro tile is found, False otherwise
        '''
        logger.info("Awaiting tile")
        # Camera looks at path
        # Once cv says "path exists" and "tile is completely set down", move to follow_path
        raise NotImplementedError
        return True

    def follow_path(self):
        '''
        This moves the Tsurobot along the current path until the path ends or is blocked.

        Returns:
            True if ending at an empty tile space, False otherwise(collision, edge of board)
        '''
        logger.info("Following path")
        # follow the path using CV (be able to correct steering for small errors, but not overcorrect)
        # once CV says "edge of board imminent", move to await_tile
        # if you see bot, move to DONE and make sad noise
        # If you see edge / start position again, move to DONE and make sad noise
        raise NotImplementedError
        return True


def play_game(tsurobot=Tsurobot(), next_game_action="look_for_board"):
    """
    This function begins game play for the Tsurobot

    Args:
        tsurobot: Your Tsurobot instance
        next_game_action: Start in a specified game state

    Returns:
        None
    """
    logger.info("Playing Tsuro with next game action: {0}".format(str(next_game_action)))
    # Here's the state machine for gameplay
    while(next_game_action):
        if next_game_action == "look_for_board":
            if tsurobot.look_for_board():
                next_game_action = "calibrate_to_board"
        elif next_game_action == "calibrate_to_board":
            if tsurobot.calibrate_to_board():
                next_game_action = "move_to_start"
            else:
                return None
        elif next_game_action == "move_to_start":
            if tsurobot.move_to_start():
                next_game_action = "await_tile"
            else:
                return None
        elif next_game_action == "await_tile":
            if tsurobot.await_tile():
                next_game_action = "follow_path"
        elif next_game_action == "follow_path":
            if tsurobot.follow_path():
                next_game_action = "await_tile"
            else:
                return None
    return None
