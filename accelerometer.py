import time
import XLoBorg


def read_adjusted_accelerometer():
    x, y, z = XLoBorg.ReadAccelerometer()
    # make adjustment for the attitude of the pibot
    x -= 0.015625
    return x, y, z

if __name__ == "__main__":
    XLoBorg.Init()
    for counter in range(200):
        x, y, z = read_adjusted_accelerometer()
        print "x: %s, y: %s, z: %s" % (x * 100, y * 100, z * 100)
        time.sleep(1)
