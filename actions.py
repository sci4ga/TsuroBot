def calibrate():
    '''
    This directs the robot to calibrate sensors relative to the start position.
    It returns the appropriate next state as a string.
    '''
    raise NotImplementedError
    return None

def approachboard():
    '''
    This directs the robot to move from start position to the edge of the tile area.
    It returns the appropriate next state as a string.
    '''
    raise NotImplementedError
    return None


def identifytile():
    '''
    This directs the robot to look for a tile played in the immediate tile area.
    It returns the appropriate next state as a string.
    '''
    raise NotImplementedError
    return None


def followpath():
    '''
    This directs the robot to folow the path until a stop condition is reached.
    It returns the appropriate next state as a string.
    '''
    raise NotImplementedError
    return None


def stopeverything():
    '''
    This directs the robot to cease all movement.
    '''
    raise NotImplementedError
    return None
