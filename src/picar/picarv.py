# import native modules
# local imports
from picar import front_wheels, back_wheels


class PicarV:
    def __init__(self, config_json):
        self.front_wheels = front_wheels.Front_Wheels(debug=False, config=config_json)
        self.back_wheels = back_wheels.Back_Wheels(debug=False, config=config_json)
        # TODO: add vertical view (tilt)
        # TODO: add horizontal view (pan)
