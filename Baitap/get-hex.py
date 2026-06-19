#truoc khi chay can chay tren terminal nhung cau lenh sau:
# 1: ir-keytable => xem ir dang o rc bao nhieu, trong may nay la rc2
# 2: sudo ir-keytable -s rc2 -p all 
# 3: ir-keytable -s rc2 -t

import evdev
import time

# 1. Tìm mắt thu hồng ngoại trong hệ thống
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
print("Chương trình phân tách mã nhiễu đang chạy...")
print("-" * 50)

last_press_time = 0
cooldown_time = 0.3  # Chống trùng mã bấm thông thường

try:
    for event in ir_device.read_loop():
        if event.type == evdev.ecodes.EV_MSC and event.code == evdev.ecodes.MSC_SCAN:
            scancode = event.value
            current_time = time.time()
            
            # TRƯỜNG HỢP 1: PHÁT HIỆN MÃ NHIỄU
            if scancode == 0x7fffffff:
                print("\n⚠️  CẢNH BÁO: TÍN HIỆU NHIỄU PHÁT SINH! (Mã: 0x7fffffff)")
                print("⏳ HỆ THỐNG KHÓA 3 GIÂY... Mọi nút bấm lúc này sẽ bị hủy bỏ.")
                
                # Dừng toàn bộ chương trình trong 3 giây
                time.sleep(3)
                
                # XÓA BUFFER: Đọc và vứt bỏ tất cả các nút bị bấm trong thời gian 3 giây khóa
                while ir_device.read_one() is not None:
                    pass
                
                print("✅ ĐÃ KHÔI PHỤC: Hệ thống mở khóa, sẵn sàng nhận lệnh mới.\n")
                
                # Cập nhật lại mốc thời gian để tránh bị dính cooldown ngay sau khi mở khóa
                last_press_time = time.time()
                continue  # Bỏ qua phần xử lý bên dưới, quay lại vòng lặp chờ tín hiệu mới

            # TRƯỜNG HỢP 2: NÚT BẤM BÌNH THƯỜNG
            if (current_time - last_press_time) > cooldown_time:
                print(f"Mã Hex nhận được: {hex(scancode)}")
                last_press_time = current_time
                
except KeyboardInterrupt:
    print("\nĐã thoát chương trình.")