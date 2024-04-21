from MMA8653FC import MMA8653FC, twos_to_decimal
import time

sensor = MMA8653FC()

sensor.set_active()

dyn_range = sensor.get_range()
sensor.reset_offsets()
a = sensor.read_register("OFF_X")
print(bin(a))

#sensor.fast_read(0)

while True:
    """x = sensor.read_register("OUT_X_MSB")
    print(bin(x))
    xb = sensor.read_register("OUT_X_LSB")
    print(bin(xb))
    num = twos_to_decimal(x,xb)
    real = num*(2*dyn_range/2**10)
    print(f"x:{real} g")"""

    """y = sensor.read_register("OUT_Y_MSB")
    yb = sensor.read_register("OUT_Y_LSB")
    num = twos_to_decimal(y,yb)
    real = num*(2*dyn_range/2**10)
    print(f"y:{real} g")

    z = sensor.read_register("OUT_Z_MSB")
    zb = sensor.read_register("OUT_Z_LSB")
    num = twos_to_decimal(z,zb)
    real = num*(2*dyn_range/2**10)
    print(f"z:{real} g")

    accel = sensor.get_acceleration()
    print(accel)"""
    #time.sleep(0.2)




