import smbus
import sys
from time import sleep

def setup_st7030():
    trials = 5
    for i in range(trials):
        try:
            c_lower = (contrast & 0xf)
            c_upper = (contrast & 0x30)>>4
            bus.write_i2c_block_data(address_st7032, register_setting, [0x38, 0x39, 0x14, 0x70|c_lower, 0x54|c_upper, 0x6c])
            sleep(0.2)
            bus.write_i2c_block_data(address_st7032, register_setting, [0x38, 0x0d, 0x01])
            sleep(0.001)
            break
        except IOError:
            if i==trials-1:
                sys.exit()
                
def clear():
    global position
    global line
    position = 0
    line = 0
    bus.write_byte_data(address_st7032, register_setting, 0xc01)
    sleep(0.001)
    
def newline():
    global position
    global line
    if line == display_lines-1:
        clear()
    else:
        line += 1
        position = chars_per_line*line
        bus.write_byte_data(address_st7032, register_setting, 0xc0)
        sleep(0.01)
    
def write_string(s):
    for c in list(s):
        write_char(ord(c))
        
def write_char(c):
    global position
    byte_data = check_writable(c)
    if position == display_chars:
        clear()
    elif position == chars_per_line*(line+1):
        newline()
    bus.write_byte_data(address_st7032, register_display, byte_data)
    position += 1
    
def check_writable(c):
    if c >= 0x06 and c <= 0xff:
        return c
    else:
        return 0x20 #ky tu khoang trang


    
bus = smbus.SMBus(1)    #kich hoat cong i2c bus 1 cua PI
address_st7032= 0x3e    # dia chi i2c cua man hinh lcd (quet ra tu lenh i2cdetect)
register_setting = 0x00 #thanh ghi nhan lenh du lieu ky tu (nhu xoa man hinh, chinh con tro)
register_display = 0x40 # thanh ghi nhan du lieu ky tu de hien thi len man hinh

contrast = 32 #do tuong phan cua man hinh (gia tri tu 0 den 63, khuyen nen de tu 30 den 40 de nhin ro chu nhat)
chars_per_line = 8 # 8 ky tu moi hang
display_lines = 2 # man hinh co 2 hang

display_chars = chars_per_line*display_lines

position = 0
line = 0

setup_st7030()

if len(sys.argv)==1:
    #write_string('bong chinh dep')
    #s = chr(0xd7) + chr(0xbd) + chr(0xde) + chr(0xcd) + chr(0xde) + chr(0xd8) + chr(0xb0) + '' + chr(0xca) + chr(0xdf) + chr(0xb2)
    s = chr(0xba) + chr(0xdd) + chr(0xa5) + chr(0xc4) + chr(0xa9) + chr(0xb2) + chr(0xa5) + chr(0xc6) + chr(0xad) + chr(0xdd)
    write_string(s)
else:
    write_string(sys.argv[1])
