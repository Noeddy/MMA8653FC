from smbus2 import SMBus

with SMBus(1) as bus:
    # Read a block of 16 bytes from address 80, offset 0
    block = bus.read_byte_data(0x1d, 0) 
    # Returned value is a list of 7 bytes
    print(block)