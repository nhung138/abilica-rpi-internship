import smbus
import sys
import time
import board
import adafruit_dht

# ==========================================
# CÁC HÀM ĐIỀU KHIỂN MÀN HÌNH (Từ code của bạn)
# ==========================================
def setup_st7030():
    trials = 5
    for i in range(trials):
        try:
            c_lower = (contrast & 0xf)
            c_upper = (contrast & 0x30) >> 4
            bus.write_i2c_block_data(address_st7032, register_setting, [0x38, 0x39, 0x14, 0x70|c_lower, 0x54|c_upper, 0x6c])
            time.sleep(0.2)
            bus.write_i2c_block_data(address_st7032, register_setting, [0x38, 0x0d, 0x01])
            time.sleep(0.001)
            break
        except IOError:
            if i == trials - 1:
                sys.exit()

def clear():
    global position
    global line
    position = 0
    line = 0
    bus.write_byte_data(address_st7032, register_setting, 0x01) # Chỉnh sửa nhẹ: Lệnh xóa màn hình là 0x01
    time.sleep(0.001)

def newline():
    global position
    global line
    if line == display_lines - 1:
        clear()
    else:
        line += 1
        position = chars_per_line * line
        bus.write_byte_data(address_st7032, register_setting, 0xc0)
        time.sleep(0.01)

def write_string(s):
    for c in list(s):
        write_char(ord(c))

def write_char(c):
    global position
    byte_data = check_writable(c)
    if position == display_chars:
        clear()
    elif position == chars_per_line * (line + 1):
        newline()
    bus.write_byte_data(address_st7032, register_display, byte_data)
    position += 1

def check_writable(c):
    if c >= 0x06 and c <= 0xff:
        return c
    else:
        return 0x20 # ky tu khoang trang

# ==========================================
# CẤU HÌNH BIẾN MÀN HÌNH
# ==========================================
bus = smbus.SMBus(1)
address_st7032 = 0x3e
register_setting = 0x00
register_display = 0x40

contrast = 32
chars_per_line = 8
display_lines = 2
display_chars = chars_per_line * display_lines

position = 0
line = 0

# ==========================================
# CHƯƠNG TRÌNH CHÍNH (ĐỌC DHT11 + HIỂN THỊ)
# ==========================================
# 1. Khởi động màn hình
setup_st7030()

# 2. Khởi tạo cảm biến DHT11 (đang nối ở GPIO 17 như đã sửa ở lỗi trước)
dht_device = adafruit_dht.DHT11(board.D20)

# In chuỗi khởi động (Mỗi dòng 8 ký tự)
clear()
write_string("Bat dau ")
write_string("do...   ")
time.sleep(2)

while True:
    try:
        # Lấy dữ liệu
        nhiet_do = dht_device.temperature
        do_am = dht_device.humidity
        
        # In ra Terminal để tiện theo dõi
        print("Độ ẩm: {} %  |  Nhiệt độ: {} *C".format(do_am, nhiet_do))

        # Format lại dữ liệu cho vừa vặn với 8 ký tự của LCD
        # Hàm ljust(8) sẽ tự động thêm dấu cách vào cuối nếu chuỗi bị thiếu, 
        # đảm bảo đủ 8 ký tự để kích hoạt hàm newline() tự động của bạn.
        str_temp = "T:{} C".format(nhiet_do).ljust(8)
        str_hum = "H:{} %".format(do_am).ljust(8)
        
        clear()
        write_string(str_temp) # Viết dòng 1 xong, nó tự nhảy xuống dòng do đủ 8 ký tự
        write_string(str_hum)  # Viết dòng 2

    except RuntimeError as error:
        print("Đang thử lại... ({})".format(error.args[0]))
        time.sleep(2.0)
        continue
    except Exception as error:
        clear()
        write_string("Loi he  ")
        write_string("thong!  ")
        dht_device.exit()
        raise error

    # Chờ 2 giây theo đúng nguyên tắc của DHT11
    time.sleep(2.0)