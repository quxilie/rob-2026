
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.virtual import GPSSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)
gps = GPSSensor(INPUT_4)

PORIH = 50
BAZA = 20
Kp = 0.5
LIMIT = 120

def obmezhyty(v):
    return max(-100, min(100, v))

time.sleep(0.5)
pochatok = time.time()

while time.time() - pochatok < LIMIT and gps.y < 85:
    v = color.reflected_light_intensity
    e = PORIH - v
    korekciya = Kp * e

    l = obmezhyty(BAZA - korekciya)
    r = obmezhyty(BAZA + korekciya)

    tank.on(SpeedPercent(l), SpeedPercent(r))

tank.off()

print("GPS y:", gps.y)
print("Час до кінця траси: %.1f с" % (time.time() - pochatok))
