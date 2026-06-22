from gpiozero import DigitalInputDevice
from datetime import datetime
import time

# Cấu hình cảm biến
tilt_sensor = DigitalInputDevice(2, pull_up=True)

print("Hệ thống nhật ký ngăn kéo đang chạy...")

def log_event():
    with open("log_mo_ngan_keo.txt", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Ngăn kéo được mở lúc: {timestamp}\n")
    print(f"Đã ghi lại: {timestamp}")

try:
    while True:
        if tilt_sensor.is_active:
            log_event()
            # Đợi một chút để tránh ghi lặp liên tục khi cửa đang mở
            time.sleep(5) 
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Dừng chương trình.")