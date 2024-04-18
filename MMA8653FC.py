from smbus2 import SMBus

class MMA8653FC():

    def __init__(self):
        self.address = 0x1d
        self.registers = {"STATUS" : 0x00,
                          "OUT_X_MSB" : 0x01,
                          "OUT_X_LSB" : 0x02,
                          "OUT_Y_MSB" : 0x03,
                          "OUT_Y_LSB" : 0x04,
                          "OUT_Z_MSB" : 0x05,
                          "OUT_Z_LSB" : 0x06,
                          "WHO_AM_I" : 0x0D,
                          "XYZ_DATA_CFG" : 0x0E,
                          "CTRL_REG1" : 0x2A,
                          "OFF_X" : 0x2F,
                          "OFF_Y" : 0x30,
                          "OFF_Z" : 0x31}
        
    def read_register(self, reg):
        """
        reads the value from the requested register and returns it 

        Args:
        reg (str):name of the requested register
        
        Returns:
        int:binary value read 
        """
        res = 0
        if reg in self.registers.keys():
            reg_num = self.registers[reg]
            with SMBus(1) as bus:
                res = bus.read_byte_data(self.address, reg_num)
        else:
            raise ValueError("The register you are trying to read does not exist")
        
        return res
    
    def write_register(self, reg, data):
        """
        writes a single byte of data to the requested register
        
        Args:
        reg (str):name of the requested register
        data (int):data to be writen 
        
        Returns:None 
        """
        if reg in self.registers.keys():
            reg_num = self.registers[reg]
            with SMBus(1) as bus:
                bus.write_byte_data(self.address, reg_num, data)
        else:
            raise ValueError("The register you are trying to write to does not exist")
        
    def read_block(self, reg, length):
        """
        reads up to 32 bytes from the start register
        
        Args:
        reg (str):name of the start register
        length(int):number of bytes to be read
        
        Returns:
        (list):list of read bytes
        """
        res = []
        if reg in self.registers.keys():
            reg_num = self.registers[reg]
            with SMBus(1) as bus:
                res = bus.read_i2c_block_data(self.address, reg_num, length)
        else:
            raise ValueError("The register you are trying to read does not exist")
        
        return res
    
    def get_range(self):
        """
        reads the dynamic range, the value can be either +- 2g, 4g, or 8g
        
        Args:None
        
        Returns:
        (int):value of the range
        """
        b = self.read_register("XYZ_DATA_CFG")

        #get the last two bits
        val = b & 0b11

        if val == 0b00:
            val = 2
        elif val == 0b01:
            val = 4
        elif val == 0b10:
            val = 8
        else:
            raise ValueError("Wrong range, reverved value for FS0/1 bits")
        
        return val
    
    def set_range(self, val):
        """
        sets the dynamic range to the specified value between +- 2g, 4g and 8g
        
        Args:
        val(int):value of the desired dynamic range
        
        Returns:None
        """
        ranges = [2,4,8]
        if val not in ranges:
            raise ValueError("The range must be either 2, 4 or 8")
        else:
            bits = [0b00, 0b01, 0b10]
            i = ranges.index(val)

            cfg = self.read_register("XYZ_DATA_CFG")

            mask = 0b11111100

            cfg &= mask #clear the last two bits

            cfg ^= bits[i] #set to the desired value

            #write the byte in standby mode
            self.set_standby()
            self.write_register("XYZ_DATA_CFG", cfg)
            self.set_active()
    
    def set_active(self):
        """
        puts the accelerometer in active mode
        
        Args:None
        
        Returns:None
        """
        val = self.read_register("CTRL_REG1")
        mask = 0b1

        if (val & mask) == 0: #if inactive
            val = val ^ mask #flip the first bit
            self.write_register("CTRL_REG1", val) #write it at the correct register

    def set_standby(self):
        """
        puts the accelerometer in standby mode
        
        Args:None
        
        Returns:None
        """
        val = self.read_register("CTRL_REG1")
        mask = 0b1

        if (val & mask) == 1: #if active
            val = val ^ mask #flip the first bit
            self.write_register("CTRL_REG1", val) #write it at the correct register
    
    def get_accel_8(self):
        """
        reads the acceleration value on 3 different axis with 8-bit resolution
        
        Args:None
        
        Returns:
        (list):list of aacceleration values in order [x,y,z]
        """
        




        



    
def twos_to_decimal(num, bits=8):
    """
    converts an 8-bit 2's complement binary number to decimal
    
    Args:
    num(int):2's complement binary number to be converted
    bits(int):length of the binary number, 8 by default
    
    Returns:
    (int):decimal number
    """
    res = 0
    max_val = 2 ** (bits - 1)
    # Check if the number is negative
    if num >= max_val:
        # Convert from two's complement to decimal
        res = num - (2 ** bits)
    
    return res