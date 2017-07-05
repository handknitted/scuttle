import time
import XLoBorg
from math import cos,sin,pi, atan2, floor, asin



class Compass:

    MAGNETIC_NORTH = 0
    BRISTOL = -2.2
    declinationAngle = BRISTOL / 1000

    #  Latitude: 51 degrees 28' 42.7" N
    #  Longitude: 2 degrees 34' 14.9" W
    #  Magnetic declination: -1 degrees 23'
    #  Declination is NEGATIVE(WEST)
    #  Inclination: 66 degrees 21'
    #  Magnetic field strength: 48684.0 nT

    def __init__(self):
        XLoBorg.Init()

    def get_compass_values_raw(self):
        return XLoBorg.ReadCompassRaw()

    def get_heading(self):
        #TODO I think I'm using the wrong x,y,z  fix that.
        # Read and render the raw compass readings, correcting by our manual calibration values
        compass = XLoBorg.ReadCompassRaw()
        print str(compass[0])+","+str(compass[1])+","+str(compass[2])
        mX = compass[0]  # - -248
        mY = compass[1]  #- 370
        mZ = compass[2]  #- 1384
        print "mX:"+str(mX)+",mY:"+str(mY)

        # Read the raw accelerometer readings
        accel = XLoBorg.ReadAccelerometer()
        print str(accel[0])+","+str(accel[1])+","+str(accel[2])
        aX = accel[0]
        aY = accel[1]
        aZ = accel[2]

        # some notes on tilt compensation
        # http://www.loveelectronics.co.uk/Tutorials/13/tilt-compensated-compass-arduino-tutorial

        # =======================================================================================
        # The following code does NOT yet work... it should but my maths is a bit screwy
        # When I manage to fix it then we'll have a compass that copes with being tilted, huzzah!
        rollRadians = asin(aY)
        pitchRadians = asin(aX)
        # up to 40 degree tilt max:
        # http://www.loveelectronics.co.uk/Tutorials/13/tilt-compensated-compass-arduino-tutorial
        cosRoll = cos(rollRadians)
        sinRoll = sin(rollRadians)
        cosPitch = cos(pitchRadians);
        sinPitch = sin(pitchRadians);

        vX = mX * cosPitch + mZ * sinPitch;
        vY = mX * sinRoll * sinPitch + mY * cosRoll - mZ * sinRoll * cosPitch;
    # =======================================================================================

        # get the heading in radians
        heading = atan2(vY, vX)

        # correct for declination -- TODO is this really right?
        heading += self.declinationAngle

        # Correct negative values
        if (heading  < 0):
            heading = heading + (2 * pi)

        # Check for wrap due to declination and compensate
        if(heading > 2*pi):
            heading -= 2*pi

        # convert to degrees
        heading = heading * 180/pi;

        # get the base degrees
        heading = floor(heading)

        print("Current heading: %s" % heading)
        return heading


if __name__ == "__main__":
    compass = Compass()
    for _ in range(200):
        compass.get_heading()
        time.sleep(1)

