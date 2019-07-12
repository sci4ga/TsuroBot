from picar import back_wheels, front_wheels

picar.setup()
db_file = "/Users/andrewtsai/personal-projects/RobotTsuro/config"
fw = front_wheels.Front_Wheels(debug=False, db=db_file)
bw = back_wheels.Back_Wheels(debug=False, db=db_file)
bw.ready()
fw.ready()

SPEED = 60
bw_status = 0

bw.speed = SPEED
bw.forward()