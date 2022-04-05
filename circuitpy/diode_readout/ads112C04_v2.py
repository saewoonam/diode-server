import board
import busio
import time
import ulab.numpy as np

class ADS112C04:
    def __init__(self, addr=64, i2c=None):
        if i2c == None:
            i2c = busio.I2C(board.SCL1, board.SDA1)
        self.i2c = i2c

        self.addr = addr
        self.bias10u()
        self.readCalibrationFile('DT670.csv')
    
    def bias10u(self):
        # set current biase to 10uA
        self.writereg(2, 1)

        # set current bias to 0
        # writereg(2, 0)

        #set output to AIN0
        self.writereg(3, 0x20)

        # set ADC to AIN2(+) AIN3(-)
        self.writereg(0, 0x60)

        # single shot
        self.writereg(1, 0)

    def readreg(self, loc):
        i2c = self.i2c
        i2c.try_lock()
        msg = 0x20 + (loc<<2)
        msg = msg.to_bytes(1,'big')
        # print(msg)
        result = bytearray(1)
        i2c.writeto_then_readfrom(self.addr, msg, result)
        # print('readreg', loc, result)
        i2c.unlock()
        return result[0]

    def writereg(self, loc, value):
        i2c = self.i2c
        i2c.try_lock()
        msg = 0x40 + (loc<<2)
        # print('cmd', hex(msg))
        i2c.writeto(self.addr, bytes([msg, value]))
        i2c.unlock()

    def readRaw(self):
        i2c = self.i2c
        reading = bytearray(2);
        i2c.try_lock()
        i2c.writeto_then_readfrom(self.addr, bytes([0x10]), reading)
        result = int.from_bytes(bytes(reading), 'big')
        i2c.unlock()
        return result

    def singleV(self):
        result = self.single()
        result = result / (1<<15) * 2.048
        return result
    
    def singleT(self):
        result = self.singleV()
        result = self.convert(result)
        return result[0]
    
    def start(self):
        i2c = self.i2c
        i2c.try_lock()
        i2c.writeto(self.addr, bytes([0x08]) )
        i2c.unlock()


    def single(self):
        self.start()
        return self.rd2()

    def rd2(self):
        while ( self.readreg(2) & (1<<7) == 0):
            pass
        return self.readRaw()

    def readBoardTemp(self):
        reg1 = self.readreg(1)
        self.writereg(1, (reg1 | 1))
        #time.sleep(0.05)
        self.start()
        #time.sleep(0.05)
        #result = (self.read(raw=True)>>2)
        result = self.rd2()
        # print('reg1', reg1, self.readreg(1), result)
        if (result & 0x8000):  # check if negative and correct
            result = result - (1<<16)
        result = (result>>2) / 32.0 
        self.writereg(1, reg1)
        return result
    
    def readCalibrationFile(self, filename):
        data = []
        with open(filename) as file:
            for line in file:
                try:
                    data.append([float(x) for x in line.rstrip().split(',')])
                except:
                    #print('bad line', line)
                    pass
        self.cal = np.array(data)
        
    def convert(self, reading):
        return np.interp(reading, self.cal[:, 1], self.cal[:, 0])
    
# print(__name__)
if __name__ == '__main__':
    if 'i2c' not in locals():
        print('i2c not defined')
        i2c=None
    adc = ADS112C04(0x40, i2c)
    # print('i2c', adc.i2c)
    i2c = adc.i2c
    # adc.bias10u()
    print(adc.singleV())
    print(adc.singleT())
"""
# set current bias to 10uA
writereg(2, 1)
# print(readreg(2))

# set current bias to 0
# writereg(2, 0)

#set output to AIN0
writereg(3, 0x20)

# set ADC to AIN2(+) AIN3(-)
writereg(0, 0x60)

# single shot
writereg(1, 0)
# continuous
# writereg(1, 8)
"""
