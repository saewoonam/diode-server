import busio
import board
class ADS112C04:
    def __init__(self, I2C_address, i2c = None):
        
        if i2c == None:
            i2c = busio.I2C(board.SCL1, board.SDA1)
        self.i2c = i2c
        
        self.addr = I2C_address
        self.temp = False

    def Start(self):
        self.i2c.try_lock()
        self.i2c.writeto(self.addr, bytes([0x08]))
        self.i2c.unlock()

    def Reset(self):
        self.i2c.try_lock()
        self.i2c.writeto(self.addr, bytes([0x06]))
        self.i2c.unlock()

    def PowerDown(self):
        self.i2c.try_lock()
        self.i2c.writetto(self.addr, bytes([0x02]))
        self.i2c.unlock()

    def ReadReg(self, RegNum):
        self.i2c.try_lock()
        i2c_cmd = 0x20 + RegNum * 4
        result = bytearray(1)
        self.i2c.writeto_then_readfrom(self.addr, bytes([i2c_cmd]), result)
        self.i2c.unlock()
        return result[0]

    def WriteReg(self, RegNum, value):
        self.i2c.try_lock()
        i2c_cmd = 0x40 + RegNum * 4
        self.i2c.writeto(self.addr, bytes([i2c_cmd, value]))
        self.i2c.unlock()

    def ReadData(self):
        self.i2c.try_lock()
        data = bytearray(2)
        self.i2c.writeto_then_readfrom(self.addr, bytes([0x10]), data)
        result = int.from_bytes(bytes(data), "big")
        result = result / 32768 * 2.048 * 1e3
        self.i2c.unlock()
        return result

    def Set(self):
        #Default Set up parameters
        self.Reset()
        self.WriteReg(0, 0x60)  #Measure Voltge through AIN2 and AIN3
        self.WriteReg(1, 0x00)  #Set Ref Voltage
        self.WriteReg(2, 0x01)  # Set IDAC1 to 10uA
        self.WriteReg(3, 0x20)  # Enable IDAC to AIN0
        
    def TemperatureSense(self, x):
        if x == 0:
            self.WriteReg( 1,  0x00 + x)
            self.temp = False
        elif x == 1:
            self.WriteReg(1,  0x00 + x)
            self.temp = True

    def TemperatureRead(self):
        if self.temp == False:
            raise Exception("Turn Temperature Sensor Mode on First")
        else:
            self.i2c.try_lock()
            temp_data = bytearray(2)
            self.i2c.writeto_then_readfrom(self.addr, bytes([0x10]), temp_data)
            temp_data = int.from_bytes(temp_data, 'big') >> 2
            print(temp_data*0.03125)
            if temp_data >> 13 == 1:
                T_out = ((0x3fff - temp_data) + 0x1 )*-0.03125 #Celsius
            elif temp_data >> 13 == 0 :
                T_out = temp_data*0.03125
            self.i2c.unlock()
        return T_out
        
    def Identify(): #EDIT ONCE KNOWN
        if self.addr == 0x40:
            name = "DT-670 40K"
        elif self.addr == 0x41:
            name = "DT-670 4K"
        elif self.addr == 0x42:
            name = "blah"
        elif self.addr == 0x43:
            name = "blah"
        elif self.addr == 0x44:
            name = "blah"
        elif self.addr == 0x45:
            name = "blah"
        return (name)
    
    
