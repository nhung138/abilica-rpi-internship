import evdev
import time

# ==========================================
# 1. TỪ ĐIỂN MAP MÃ HEX VỚI NÚT TRÊN CAR MP3
# ==========================================
CAR_MP3_BUTTONS = {
    0x45: "CH-",
    0x46: "CH",
    0x47: "CH+",
    0x44: "PREV (|<<)",
    0x40: "NEXT (>>|)",
    0x43: "PLAY/PAUSE (>||)",
    0x07: "VOL-",
    0x15: "VOL+",
    0x09: "EQ",
    0x16: "0",
    0x19: "100+",
    0x0d: "200+",
    0x0c: "1",
    0x18: "2",
    0x5e: "3",
    0x08: "4",
    0x1c: "5",
    0x5a: "6",
    0x42: "7",
    0x52: "8",
    0x4a: "9"
}

# 2. Tìm mắt thu hồng ngoại trong hệ thống
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
ir_device = None

for device in devices:
    if device.name == "gpio_ir_recv":
        ir_device = device
        break

if ir_device is None:
    print("Lỗi: Không tìm thấy mắt thu hồng ngoại.")
    exit()

print(f"Đã kết nối thành công với: {ir_device.name}")
print("Chương trình nhận diện Remote Car MP3 đang chạy...")
print("-" * 55)

last_press_time = 0
cooldown_time = 0.3  # Khoảng thời gian chặn tín hiệu lặp lại khi nhấn giữ

try:
    for event in ir_device.read_loop():
        if event.type == evdev.ecodes.EV_MSC and event.code == evdev.ecodes.MSC_SCAN:
            scancode = event.value
            current_time = time.time()
            
            # TRƯỜNG HỢP 1: PHÁT HIỆN MÃ NHIỄU
            if scancode == 0x7fffffff:
                print("\n⚠️  CẢNH BÁO: TÍN HIỆU NHIỄU TỪ MÔI TRƯỜNG!")
                print("⏳ HỆ THỐNG KHÓA 3 GIÂY...")
                
                time.sleep(3)
                
                # Xóa sạch hàng đợi sự kiện phát sinh trong lúc khóa
                while ir_device.read_one() is not None:
                    pass
                
                print("✅ MỞ KHÓA: Sẵn sàng nhận lệnh mới.\n")
                
                last_press_time = time.time()
                continue

            # TRƯỜNG HỢP 2: BẤM NÚT BÌNH THƯỜNG
            # Chỉ xử lý nếu khoảng cách giữa 2 lần nhận lệnh lớn hơn cooldown_time
            if (current_time - last_press_time) > cooldown_time:
                button_name = CAR_MP3_BUTTONS.get(scancode, f"Nút chưa biết (Mã Hex: {hex(scancode)})")
                print(f"▶️ Bạn vừa bấm: [{button_name}] (Hex: {hex(scancode)})")
                
                last_press_time = current_time
                
except KeyboardInterrupt:
    print("\nĐã thoát chương trình.")