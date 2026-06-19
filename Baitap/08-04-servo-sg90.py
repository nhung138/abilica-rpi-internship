from gpiozero import AngularServo
from time import sleep

# Khởi tạo Servo tại chân GPIO 18
# Định nghĩa xung chuẩn của SG90: 1ms ứng với -90 độ, 2ms ứng với 90 độ
servo = AngularServo(18, min_angle= -90, max_angle = 90, 
                     min_pulse_width=0.7/1000, max_pulse_width=2.5/1000)

print("Hệ thống điều khiển Servo SG90 đã sẵn sàng!")
print("Nhấn Ctrl + C để dừng chương trình.")

try:
    while True:
        # 1. Quay hết cỡ sang trái (-90 độ)
        print("Quay sang trái...")
        servo.angle = -90
        sleep(1) # Đợi 1 giây cho bánh răng kịp quay đến vị trí
        
        # 2. Quay về chính giữa (0 độ)
        print("Về chính giữa...")
        servo.angle = 0
        sleep(1)
        
        # 3. Quay hết cỡ sang phải (90 độ)
        print("Quay sang phải...")
        servo.angle = 90
        sleep(1)
        
        # 4. Quay về chính giữa (0 độ)
        print("Về chính giữa...")
        servo.angle = 0
        sleep(1)
        
        
        servo.angle = 45
        sleep(1)
        
        servo.angle = -45
        sleep(1)
        
        servo.angle = 60
        sleep(1)

except KeyboardInterrupt:
    print("\nĐang dừng chương trình...")
    servo.detach() # Ngắt xung để giải phóng Servo, giúp động cơ không bị nóng khi nghỉ
    print("Đã tắt Servo an toàn!")