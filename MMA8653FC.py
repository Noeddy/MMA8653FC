from smbus2 import SMBus

def twos_to_decimal(hi, low, bits=10):
    """
    converts an 8-bit 2's complement binary number to decimal
    
    Args:
    num(int):2's complement binary number to be converted
    bits(int):length of the binary number, 10 by default
    
    Returns:
    (int):decimal number
    """
    low = (low >> 6)
    res = (hi << (bits-8)) | low #combine the high and low bytes

    if hi >= 128: #if negative
        res = ~res +1 #compute the two's complement
        
    return res

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
                          "CTRL_REG2" : 0x2B,
                          "CTRL_REG3" : 0x2C,
                          "CTRL_REG4" : 0x2D,
                          "CTRL_REG5" : 0x2E,
                          "OFF_X" : 0x2F,
                          "OFF_Y" : 0x30,
                          "OFF_Z" : 0x31}
        
        self.dyn_range = self.get_range()
        
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
        if val != self.dyn_range:
            if val not in ranges:
                raise ValueError("The range must be either 2, 4 or 8")
            else:
                bits = [0b00, 0b01, 0b10]
                i = ranges.index(val)

                cfg = self.read_register("XYZ_DATA_CFG")

                mask = 0b11111100

                cfg &= mask #clear the last two bits

                cfg ^= bits[i] #set to the desired value

                self.dyn_range = val

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

    def is_active(self):
        """
        checks if the device is active
        
        Args:None
        Returns: 
        (bool):wether device active or not
        """
        val = self.read_register("CTRL_REG1")
        mask = 0b1

        return (val & mask) == 1
    
    def fast_read(self, val):
        """
        sets fast read to on or off
        Args:
        val(int): 0 to disable 1 to enable fast read
        Returns:None
        """
        if val in [0,1]:
            ctrl = self.read_register("CTRL_REG1")
            mask = 0b10
            if (ctrl & mask)>>1 != val: 
                ctrl ^= mask #flips the F_READ bit

                self.set_standby()
                self.write_register("CTRL_REG1", ctrl)
                self.set_active()
        else:
            raise ValueError("Value of the argument must be either 0 or 1")
    
    def get_acceleration(self):
        """
        reads the acceleration value on 3 different axis with 10-bit resolution.
        
        Args:None
        
        Returns:
        (list):list of acceleration values in order [x,y,z]
        """
        status = self.read_register("STATUS")
        if (status & 0b100)>>2 == 1: #checks if ZYXDR is set
            self.fast_read(0)
            real = self.read_block("OUT_X_MSB", 6)
            res = []


            for i in [0,2,4]:
                hi = real[i]
                low = real[i+1]

                counts = twos_to_decimal(hi, low)
                val = round(counts*(self.dyn_range/512), 3)

                res.append(val)
        
        else:
            raise RuntimeError("No new data to read, try activating the device with MMA8653FC.set_active()")

        return res
    
    def set_offset_x(self, val):
        """
        sets the x-axis offset
        Args:
        val(float): value of the offset
        Returns:None
        """
        counts = round((512*val)/self.dyn_range) #convert to the number of counts
        mask = 0b1111111100 
        counts = (counts & mask) >> 2 #keep only the 8 most significant bits
        
        #write it to the
        self.set_standby()
        self.write_register("OFF_X",counts)
        self.set_active()

    def set_offset_y(self, val):
        """
        sets the y-axis offset
        Args:
        val(float): value of the offset
        Returns:None
        """
        counts = round((512*val)/self.dyn_range) #convert to the number of counts
        mask = 0b1111111100 
        counts = (counts & mask) >> 2 #keep only the 8 most significant bits
        
        #write it to the
        self.set_standby()
        self.write_register("OFF_Y",counts)
        self.set_active()

    def set_offset_z(self, val):
        """
        sets the z-axis offset
        Args:
        val(float): value of the offset
        Returns:None
        """
        counts = round((512*val)/self.dyn_range) #convert to the number of counts
        mask = 0b1111111100 
        counts = (counts & mask) >> 2 #keep only the 8 most significant bits
        
        #write it to the
        self.set_standby()
        self.write_register("OFF_Z",counts)
        self.set_active()

    def reset_offsets(self):
        """
        resets all offset values
        Args:None
        Returns:None
        """
        self.set_offset_x(0)
        self.set_offset_y(0)
        self.set_offset_z(0)
        
        