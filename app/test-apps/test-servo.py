import sys
from adafruit_servokit import ServoKit
import datetime

print('Running ', datetime.datetime.now())

kit = ServoKit(channels=16)

print('initialized servo hat')

angle = int(sys.argv[1])

kit.servo[0].angle = angle
kit.servo[1].angle = angle
kit.servo[2].angle = angle
