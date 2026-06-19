import smbus
from time import sleep

def read_adt7410():
    word_data = bus.read_word_data(address_adt7410, register_adt7410)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
    data = data>>3 # 13 bit data
    if data & 0x1000 == 0: #truong hop nhiet do chinh xac bang 0
        temperature = data*0.0625
    else:
        temperature = ( (~data&0x1fff) + 1)* -0.0625
    return temperature

bus = smbus.SMBus(1)
address_adt7410 = 0x48
register_adt7410 = 0x00

try:
    while True:
        inputValue = read_adt7410()
        print(inputValue)
        sleep(0.5)
    
except KeyboardInterrupt:
    pass






