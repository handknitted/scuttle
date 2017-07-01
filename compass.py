import time
import XLoBorg
from math import cos,sin,pi, atan2, floor, asin

class Compass:

    BRISTOL = -2.2
    declinationAngle = BRISTOL / 1000

    def __init__(self):
        XLoBorg.Init()

    def get_heading(self):
        #TODO I think I'm using the wrong x,y,z  fix that.
        # Read and render the raw compass readings, correcting by our manual calibration values
        compass = XLoBorg.ReadCompassRaw()
        print str(compass[0])+","+str(compass[1])+","+str(compass[2])
        mX = compass[0] - -248
        mY = compass[1] - 370
        mZ = compass[2] - 1384
        # print "mX:"+str(mX)+",mY:"+str(mY)

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
        heading = atan2(vY,vX)

        # correct for declination
        heading += self.declinationAngle

        # Correct negative values
        if (heading < 0):
            heading = heading + (2 * pi)

        # Check for wrap due to declination and compensate
        if(heading > 2*pi):
            heading -= 2*pi

        # convert to degrees
        heading = heading * 180/pi;

        # get the base degrees
        heading = floor(heading)
        return heading

        # angle = heading*pi*2/360
        # ox = 165
        # oy = 165
        # x = ox + self.size*sin(angle)*0.45
        # y = oy - self.size*cos(angle)*0.45
        # self.w.coords("compass", (ox,oy,x,y))
        #
        # angleTarget = targetDirection*pi*2/360
        # xt = ox + self.size*sin(angleTarget)*0.45
        # yt = oy - self.size*cos(angleTarget)*0.45
        # self.w.coords("target", (ox,oy, xt, yt))
        #
        # gapAngle = abs(targetDirection - heading) # we want the angle without the sign
        # # if the gap angle is more than 180 degrees away then it is closer than we think
        # if gapAngle > 180 :
        # gapAngle = 360-gapAngle
        # if gapAngle < 0 :
        #     print "Target is " + str(gapAngle) + " degrees anticlockwise"
        # elif gapAngle > 0 :
        #     print "Target is " + str(gapAngle) + " degrees clockwise"
        # else:
        #     print "Target acquired!"
        #
        # self.after(500, self.update_compass)


if __name__ == "__main__":
    compass = Compass()
    for _ in range(20):
        x = compass.get_heading()
        print("Heading: %s" % x)
        time.sleep(1)

