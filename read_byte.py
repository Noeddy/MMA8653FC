from MMA8653FC import MMA8653FC, twos_to_decimal
import time

sensor = MMA8653FC()
sensor.set_active()

dyn_range = sensor.get_range()

a = sensor.read_register("CTRL_REG1")
print(bin(a))

sensor.fast_read(0)
print(bin(a))



while True:
    """z = sensor.read_register("OUT_Y_MSB")
    print("z:"+bin(z))
    zb = sensor.read_register("OUT_Y_LSB")
    print("zb:"+bin(zb))

    num = twos_to_decimal(z,zb)
    print(num)
    real = num*(2*dyn_range/2**10)
    print(f"{real} g")"""
    accel = sensor.get_acceleration()
    print(accel)
    time.sleep(0.2)




