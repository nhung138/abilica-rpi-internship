import smbus
import sys
import time
import evdev

# ==========================================
# 1. CẤU HÌNH VÀ HÀM ĐIỀU KHIỂN LCD ST7030/ST7032
# ==========================================
bus = smbus.SMBus(1)
address_st7032 = 0x3e
register_setting = 0x00
register_display = 0x40

contrast = 32
chars_per_line = 8  # Màn hình 8 ký tự/dòng
display_lines = 2   # Màn hình 2 dòng
display_chars = chars_per_line * display_lines

position = 0
line = 0

def setup_st7030():
    trials = 5
    for i in range(trials):
        try:
            c_lower = (contrast & 0xf)
            c_upper = (contrast & 0x30) >> 4
            bus.write_i2c_block_data(address_st7032, register_setting, [0x38, 0x39, 0x14, 0x70|c_lower, 0x54|c_upper, 0x6c])
            time.sleep(0.2)
            bus.write_i2c_block_data(address_st7032, register_setting, [0x38, 0x0c, 0x01]) # Đổi 0x0d thành 0x0c để tắt nhấp nháy con trỏ
            time.sleep(0.001)
            break
        except IOError:
            if i == trials - 1:
                print("Lỗi: Không tìm thấy màn hình LCD!")
                sys.exit()

def clear():
    global position, line
    position = 0
    line = 0
    # Đã sửa lỗi 0xc01 thành 0x01 (Lệnh xóa màn hình chuẩn)
    bus.write_byte_data(address_st7032, register_setting, 0x01)
    time.sleep(0.005)

def newline():
    global position, line
    if line == display_lines - 1:
        clear()
    else:
        line += 1
        position = chars_per_line * line
        bus.write_byte_data(address_st7032, register_setting, 0xc0) # Lệnh xuống dòng
        time.sleep(0.01)

def write_string(s):
    for c in list(s):
        write_char(ord(c))

def write_char(c):
    global position, line
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
        return 0x20

# ==========================================
# 2. MAP NÚT REMOTE VÀ KHỞI TẠO HỒNG NGOẠI
# ==========================================
CAR_MP3_BUTTONS = {
    0x45: "CH-", 0x46: "CH", 0x47: "CH+",
    0x44: "PREV", 0x40: "NEXT", 0x43: "PLAY/PAUSE",
    0x07: "VOL-", 0x15: "VOL+", 0x09: "EQ",
    0x16: "0", 0x19: "100+", 0x0d: "200+",
    0x0c: "1", 0x18: "2", 0x5e: "3",
    0x08: "4", 0x1c: "5", 0x5a: "6",
    0x42: "7", 0x52: "8", 0x4a: "9"
}

# Khởi chạy LCD trước
setup_st7030()
clear()
write_string("IR READY") # Vừa đúng 8 ký tự

# Quét tìm thiết bị hồng ngoại
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
ir_device = next((device for device in devices if device.name == "gpio_ir_recv"), None)

if ir_device is None:
    print("Lỗi: Không tìm thấy mắt thu hồng ngoại.")
    clear()
    write_string("NO IR !")
    sys.exit()

print("-" * 50)
print("Chương trình đang lắng nghe...")

last_press_time = 0
cooldown_time = 0.3

# ==========================================
# 3. VÒNG LẶP XỬ LÝ CHÍNH
# ==========================================
try:
    for event in ir_device.read_loop():
        if event.type == evdev.ecodes.EV_MSC and event.code == evdev.ecodes.MSC_SCAN:
            scancode = event.value
            current_time = time.time()
            
            # TRƯỜNG HỢP: MÃ NHIỄU
            if scancode == 0x7fffffff:
                print("⚠️ NHIỄU: Hệ thống khóa 3 giây...")
                
                # Hiển thị cảnh báo lên LCD
                clear()
                write_string("WARNING!")
                newline()
                write_string("NOISE...")
                
                time.sleep(3)
                
                # Xả hàng đợi
                while ir_device.read_one() is not None:
                    pass
                
                # Trả lại trạng thái màn hình
                clear()
                write_string("IR READY")
                
                last_press_time = time.time()
                continue

            # TRƯỜNG HỢP: NÚT BẤM BÌNH THƯỜNG
            if (current_time - last_press_time) > cooldown_time:
                button_name = CAR_MP3_BUTTONS.get(scancode, "UNKNOWN")
                print(f"▶️ Bạn vừa bấm: [{button_name}]")
                
                # Hiển thị lên LCD (Ví dụ: Dòng 1 "BTN:", Dòng 2 tên nút)
                clear()
                write_string("Button:")
                newline()
                
                # Cắt chuỗi để đảm bảo không bị tràn quá 8 ký tự của dòng 2
                write_string(button_name[:8]) 
                
                last_press_time = current_time
                
except KeyboardInterrupt:
    clear()
    print("\nĐã thoát chương trình.")