from gpiozero import DigitalInputDevice, Buzzer
from time import sleep

# Cấu hình chân
# Cảm biến nghiêng ở GPIO 2
tilt_sensor = DigitalInputDevice(2, pull_up=True)
# Buzzer ở GPIO 17
buzzer = Buzzer(17)

print("Hệ thống cảnh báo bằng âm thanh đã sẵn sàng...")

try:
    while True:
        if tilt_sensor.is_active:
            print("Đang nghiêng! Còi báo động!")
            buzzer.on()  # Bật còi
            sleep(0.2)   # Còi kêu trong 0.2 giây
            buzzer.off() # Tắt còi
        else:
            # Nếu không nghiêng, đảm bảo còi tắt
            buzzer.off()
        
        sleep(0.1) # Độ trễ nhỏ để tránh quá tải CPU
except KeyboardInterrupt:
    buzzer.off()
    print("\nĐã dừng chương trình.")