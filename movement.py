import compass
import time


def turn_to_bearing(compass_tool, desired_heading):
    correct = None
    while not correct:
        current_bearing = compass_tool.get_heading()
        correct = current_bearing == desired_heading
        turn = desired_heading - current_bearing
        alternative_turn = desired_heading - current_bearing + 360
        if abs(turn) > abs(alternative_turn):
            best_turn = alternative_turn
        else:
            best_turn = turn
        if best_turn > 0:
            direction = "right"
        elif best_turn < 0:
            direction = "left"
        else:
            direction = "not"
        print("Turn me %s!" % direction)
        time.sleep(0.5)

if __name__ == "__main__":
    my_compass = compass.Compass()
    direction = 100
    while direction != 0:
        direction = my_compass.which_way_to_bearing(97)
        print("Need to turn %d" % direction)
        time.sleep(0.5)
