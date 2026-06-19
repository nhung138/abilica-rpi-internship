from gpiozero import DigitalInputDevice
from time import sleep

# Khai báo cảm biến ở chân GPIO 2 (chân số 3 vật lý)
# pull_up=True giúp ổn định tín hiệu nếu module của bạn là dạng "pull-down"
tilt_sensor = DigitalInputDevice(2, pull_up=True)

print("Đang bắt đầu kiểm tra cảm biến... (Nhấn Ctrl+C để dừng)")

try:
    while True:
        if tilt_sensor.is_active:
            # Tùy vào module, trạng thái active có thể là đang nghiêng hoặc đang đứng yên
            print("Trạng thái: Đang nghiêng/Đang kích hoạt")
        else:
            print("Trạng thái: Bình thường (không nghiêng)")
            
        sleep(0.5) # Đợi 0.5 giây để tránh làm tràn màn hình terminal

except KeyboardInterrupt:
    print("\nĐã dừng chương trình.")