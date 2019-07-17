# import native modules
# local imports
import picar


class PicarV:
    def __init__(self, db_file):
        self.front_wheels = picar.front_wheels.Front_Wheels(debug=False, db=db_file)
        self.back_wheels = picar.back_wheels.Back_Wheels(debug=False, db=db_file)
        # TODO: add vertical view
        # TODO: add horizontal view
        self.front_wheels.ready()
        self.back_wheels.ready()
        picar.setup()
