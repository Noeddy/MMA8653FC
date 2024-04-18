from MMA8653FC import MMA8653FC, twos_to_decimal
import time

sensor = MMA8653FC()

a = sensor.read_register("OUT_Z_MSB")
print(bin(a))

a = twos_to_decimal(a)
print(a)