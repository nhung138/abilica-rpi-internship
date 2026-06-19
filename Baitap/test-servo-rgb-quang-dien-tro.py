from gpiozero import MCP3208, RGBLED, Servo
from time import sleep
from datetime import datetime

# --- Cấu hình phần cứng ---
# MCP3208 nối qua SPI, channel 0 đọc cảm biến ánh sáng
adc = MCP3208(channel=0)
led = RGBLED(red=26, green=19, blue=3)
# Servo nối với GPIO 18
roof_servo = Servo(18)

def get_light_value():
    """Lọc nhiễu: lấy trung bình cộng của 5 lần đọc"""
    values = [adc.value for _ in range(5)]
    return sum(values) / len(values) * 10000

def update_system():
    light_val = get_light_value()
    now = datetime.now().time()
    
    # Định nghĩa khung giờ ngày
    day_start = datetime.strptime("06:00", "%H:%M").time()
    day_end = datetime.strptime("17:00", "%H:%M").time()

    if day_start <= now <= day_end:
        # TRẠNG THÁI BAN NGÀY
        if light_val > 5000:
            led.color = (1, 0, 0)      # Đỏ: Nắng gắt
            roof_servo.min()           # Đóng mái
            print(f"Nắng gắt ({light_val:.0f}): Đang đóng mái.")
        else:
            led.color = (0, 1, 0)      # Xanh lá: Trời râm
            roof_servo.max()           # Mở mái
            print(f"Trời râm ({light_val:.0f}): Đang mở mái.")
    else:
        # TRẠNG THÁI BAN ĐÊM (17:01 - 05:59)
        led.color = (0, 0, 1)          # Xanh dương: Trời tối
        roof_servo.min()               # Đóng mái để giữ nhiệt/an toàn
        print(f"Ban đêm ({light_val:.0f}): Đã đóng mái.")

# --- Vòng lặp chính ---
try:
    print("Hệ thống đang chạy... Nhấn Ctrl+C để dừng.")
    while True:
        update_system()
        sleep(2) # Thời gian trễ giữa các lần kiểm tra
except KeyboardInterrupt:
    print("\nĐang dừng hệ thống...")
finally:
    # Giải phóng tài nguyên
    led.off()
    roof_servo.detach()
    print("Đã đóng an toàn.")