from MMA8653FC import MMA8653FC, twos_to_decimal
import time

sensor = MMA8653FC()

sensor.set_active()

while True:

    accel = sensor.get_acceleration()
    print(accel)
    time.sleep(0.2)