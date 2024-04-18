from MMA8653FC import MMA8653FC, twos_to_decimal
import time

sensor = MMA8653FC()

a = sensor.get_range()
print(a)

sensor.set_range(4)

a = sensor.get_range()
print(a)

sensor.set_range(2)

a = sensor.get_range()
print(a)
