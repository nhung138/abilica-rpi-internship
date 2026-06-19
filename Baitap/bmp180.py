#cam bien do ap suat, nhietdo, do cao

import smbus2
import time

bus = smbus2.SMBus(1)
ADDR = 0x77

def read_cal():
    data = bus.read_i2c_block_data(ADDR, 0xAA, 22)
    def s16(i): return i if i < 32768 else i - 65536
    return [s16((data[i*2] << 8) | data[i*2+1]) for i in range(11)]

def read_raw(reg, bytes_num):
    bus.write_byte_data(ADDR, 0xF4, reg)
    time.sleep(0.05)
    d = bus.read_i2c_block_data(ADDR, 0xF6, bytes_num)
    if bytes_num == 2:
        return (d[0] << 8) | d[1]
    else:
        return ((d[0] << 16) | (d[1] << 8) | d[2]) >> 8

def get_data(cal):
    AC1, AC2, AC3, AC4, AC5, AC6, B1, B2, MB, MC, MD = cal
    UT = read_raw(0x2E, 2)
    UP = read_raw(0x34, 3)

    # 1. Nhiệt độ
    X1 = ((UT - AC6) * AC5) >> 15
    X2 = (MC << 11) // (X1 + MD)
    B5 = X1 + X2
    temp = ((B5 + 8) >> 4) / 10.0
    
    # 2. Áp suất (Sử dụng ép kiểu để tránh số âm)
    B6 = B5 - 4000
    X1 = (B2 * (B6**2 >> 12)) >> 11
    X2 = (AC2 * B6) >> 11
    X3 = X1 + X2
    
    # B3 phải là kết quả của phép toán nguyên có dấu
    B3 = (((AC1 * 4 + X3) << 0) + 2) >> 2
    
    X1 = (AC3 * B6) >> 13
    X2 = (B1 * (B6**2 >> 12)) >> 16
    X3 = ((X1 + X2) + 2) >> 2
    B4 = (AC4 * (X3 + 32768)) >> 15
    
    # B7 là giá trị trung gian quan trọng, cần đảm bảo không tràn số
    B7 = (UP - B3) * 50000
    
    # Tính p và đảm bảo giá trị tuyệt đối
    p = (B7 * 2) // B4
    
    X1 = (p >> 8)**2
    X1 = (X1 * 3038) >> 16
    X2 = (-7357 * p) >> 16
    p = p + ((X1 + X2 + 3791) >> 4)
    
    # Ép kiểu kết quả cuối cùng sang hPa (dương)
    return temp, abs(p) / 100.0

cal = read_cal()

while True:
    try:
        t, p = get_data(cal)
        print(f"Nhiệt độ: {t:.1f} °C | Áp suất: {p:.2f} hPa")
        time.sleep(2)
    except Exception as e:
        print(f"Lỗi: {e}")
        time.sleep(1)