from picar import back_wheels, front_wheels

db_file = "/home/pi/RobotTsuro/_test_scripts/config"
fw = front_wheels.Front_Wheels(debug=False, db=db_file)
bw = back_wheels.Back_Wheels(debug=False, db=db_file)

SPEED = 60
bw_status = 0

def run(action):
    global SPEED, bw_status
    debug = ''
    # ============== Back wheels =============
    if action == 'bwready':
        bw.ready()
        bw_status = 0
    elif action == 'forward':
        bw.speed = SPEED
        bw.forward()
        bw_status = 1
        debug = "speed =", SPEED
    elif action == 'backward':
        bw.speed = SPEED
        bw.backward()
        bw_status = -1
    elif action == 'stop':
        bw.stop()
        bw_status = 0

    # ============== Front wheels =============
    elif action == 'fwready':
        fw.ready()
    elif action == 'fwleft':
        fw.turn_left()
    elif action == 'fwright':
        fw.turn_right()
    elif action == 'fwstraight':
        fw.turn_straight()
    elif 'fwturn' in action:
        print("turn %s" % action)
        fw.turn(int(action.split(':')[1]))
    
    # ================ Camera =================
    elif action == 'camready':
        cam.ready()
    elif action == "camleft":
        cam.turn_left(40)
    elif action == 'camright':
        cam.turn_right(40)
    elif action == 'camup':
        cam.turn_up(20)
    elif action == 'camdown':
        cam.turn_down(20)
    elif 'speed' in action:
		speed = int(action.split(':')[1])
		if speed < 0:
			speed = 0
		if speed > 100:
			speed = 100
		SPEED = speed
		if bw_status != 0:
			bw.speed = SPEED
		debug = "speed =", speed
    
bw.ready()
bw_status = 0
while True:
    bw.speed = SPEED
    bw.forward()
    bw.status = 1