import time
import XLoBorg
from math import cos, sin, pi, atan2, floor, asin


class Compass:

    MAGNETIC_NORTH = 0
    BRISTOL = -1
    declinationAngle = BRISTOL / 1000

    #  Latitude: 51 degrees 28' 42.7" N
    #  Longitude: 2 degrees 34' 14.9" W
    #  Magnetic declination: -1 degrees 23'
    #  Declination is NEGATIVE(WEST)
    #  Inclination: 66 degrees 21'
    #  Magnetic field strength: 48684.0 nT

    def __init__(self):
        XLoBorg.Init()
        self.needle = XLoBorg



    def get_compass_bearing(self):
        raw = self.needle.ReadCompassRaw()
         # get the heading in radians
        heading = atan2(raw[1], raw[y])

        # Correct negative values
        if heading < 0:
            heading = heading + (2 * pi)

        # convert to degrees
        return heading * 180 / pi


    def get_heading(self):
        #TODO I think I'm using the wrong x,y,z  fix that.
        # Read and render the raw compass readings, correcting by our manual calibration values
        readings = self.needle.ReadCompassRaw()
        mX = readings[0] - 392.275
        mY = readings[1] - 1014.4
        mZ = readings[2] - 2218.6
        print "mX:"+str(mX)+",mY:"+str(mY)

        # Read the raw accelerometer readings
        accel_x, accel_y, accel_z = self.needle.ReadAccelerometer()

        # some notes on tilt compensation
        # http://www.loveelectronics.co.uk/Tutorials/13/tilt-compensated-compass-arduino-tutorial

        # =======================================================================================
        # The following code does NOT yet work... it should but my maths is a bit screwy
        # When I manage to fix it then we'll have a compass that copes with being tilted, huzzah!
        rollRadians = asin(accel_y)
        pitchRadians = asin(accel_x)
        # up to 40 degree tilt max:
        # http://www.loveelectronics.co.uk/Tutorials/13/tilt-compensated-compass-arduino-tutorial
        cosRoll = cos(rollRadians)
        sinRoll = sin(rollRadians)
        cosPitch = cos(pitchRadians)
        sinPitch = sin(pitchRadians)

        vX = mX * cosPitch + mZ * sinPitch
        vY = mX * sinRoll * sinPitch + mY * cosRoll - mZ * sinRoll * cosPitch
    # =======================================================================================

        # get the heading in radians
        heading = atan2(vY, vX)

        # correct for declination -- TODO is this really right?
        heading += self.declinationAngle

        # Correct negative values
        if heading < 0:
            heading = heading + (2 * pi)

        # Check for wrap due to declination and compensate
        if heading > 2*pi:
            heading -= 2*pi

        # convert to degrees
        heading = heading * 180/pi

        # get the base degrees
        heading = floor(heading)

        print("Current heading: %s" % heading)
        return heading

    def which_way_to_bearing(self, desired_heading):
        current_bearing = self.get_heading()
        turn = desired_heading - current_bearing
        alternative_turn = desired_heading - current_bearing + 360
        if abs(turn) > abs(alternative_turn):
            best_turn = alternative_turn
        else:
            best_turn = turn
        return best_turn

if __name__ == "__main__":

    compass = Compass()

    for _ in range(200):
        print ("Bearing: %s" % str(compass.get_compass_bearing())
        time.sleep(1)

