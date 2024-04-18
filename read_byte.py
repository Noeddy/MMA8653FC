from MMA8653FC import MMA8653FC, twos_to_decimal
import time

sensor = MMA8653FC()
sensor.set_active()

dyn_range = sensor.get_range()

a = sensor.read_register("CTRL_REG1")
print(bin(a))
b = sensor.read_register("STATUS")
print(bin(b))

while True:
    z = sensor.read_register("OUT_Z_MSB")
    #print(bin(z))
    zb = sensor.read_register("OUT_Z_LSB")
    #print(bin(zb))

    combined = (z << 8) | zb
    #print(bin(combined))
    mask = 0b1111111111000000
    cleared = (combined & mask) >> 6
    #print(bin(cleared))
    num = twos_to_decimal(cleared)
    #print(num)
    num = num/256

    print(num)
    time.sleep(0.05)




