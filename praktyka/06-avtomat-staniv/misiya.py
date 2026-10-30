
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
ultra = UltrasonicSensor(INPUT_2)
gyro = GyroSensor(INPUT_3)

time.sleep(0.5)

stan = "poshuk"
vkhid = time.time()


def perekhid(novyi):
    """Зміна стану, повідомлення в консолі та дії при вході."""
    global stan, vkhid

    print(f"{stan} -> {novyi}")

    stan = novyi
    vkhid = time.time()

    if novyi == "poshuk":
        print("Поточна дія: робот шукає перешкоду")
    elif novyi == "pidhid":
        print("Поточна дія: робот повільно наближається")
    elif novyi == "rozvorot":
        print("Поточна дія: робот розвертається")
        gyro.reset()
    elif novyi == "gotovo":
        print("Поточна дія: місію завершено")


print("Поточний стан: poshuk — робот шукає перешкоду")

while stan != "gotovo":

    d = ultra.distance_centimeters

    if stan == "poshuk":
        tank.on(SpeedPercent(30), SpeedPercent(30))

        if d < 45:
            perekhid("pidhid")

    elif stan == "pidhid":
        tank.on(SpeedPercent(10), SpeedPercent(10))

        if d < 15:
            perekhid("rozvorot")

    elif stan == "rozvorot":
        tank.on(SpeedPercent(20), SpeedPercent(-20))

        if gyro.angle >= 180:
            tank.off()
            perekhid("gotovo")

    # Таймаут: якщо стан триває довше 20 секунд
    if time.time() - vkhid > 20:
        print("таймаут у стані", stan)
        tank.off()
        break

tank.off()
print("Роботу завершено.")

