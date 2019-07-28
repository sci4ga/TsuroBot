# import native modules
# local imports
import picar


class PicarV:
    def __init__(self, config_json):
        self.front_wheels = picar.front_wheels.Front_Wheels(debug=False, config=config_json)
        self.back_wheels = picar.back_wheels.Back_Wheels(debug=False, config=config_json)
        # TODO: add vertical view (tilt)
        # TODO: add horizontal view (pan)
        self.front_wheels.ready()
        self.back_wheels.ready()
        picar.setup()
