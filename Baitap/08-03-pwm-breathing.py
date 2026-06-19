from gpiozero import PWMLED
from time import sleep

# Khởi tạo đèn LED tại chân GPIO 25 sử dụng lớp đối tượng PWM
led = PWMLED(25)

print("Hệ thống đang kích hoạt hiệu ứng Đèn LED thở...")
print("Hãy quan sát bóng LED trên Breadboard. Nhấn Ctrl + C để dừng lại.")

try:
    while True:
        # -----------------------------------------------------------------
        # CHIỀU 1: SÁNG DẦN LÊN (Tăng Duty Cycle từ 0% lên 100%)
        # -----------------------------------------------------------------
        # Hàm range(0, 101) sẽ chạy từ số 0 đến số 100
        for brightness in range(0, 101):
            # Lớp PWMLED yêu cầu giá trị từ 0.0 đến 1.0
            # Ta lấy số nguyên chia cho 100.0 để ra số thực (Ví dụ: 50 / 100.0 = 0.5)
            led.value = brightness / 100.0
            
            # Giữ mức độ sáng này trong 10 mili giây để mắt người kịp cảm nhận
            sleep(0.01)
            
        # -----------------------------------------------------------------
        # CHIỀU 2: MỜ DẦN ĐI (Giảm Duty Cycle từ 100% xuống 0%)
        # -----------------------------------------------------------------
        # Vòng lặp lùi: Bắt đầu từ 100, lùi về 0, mỗi bước trừ đi 1 đơn vị (-1)
        for brightness in range(100, -1, -1):
            led.value = brightness / 100.0
            sleep(0.01)

except KeyboardInterrupt:
    # Bẫy lỗi khi bạn bấm nút Stop màu đỏ trên Thonny hoặc gõ Ctrl + C
    print("\n[Thông báo] Đang dừng chương trình...")
    led.value = 0.0  # Tắt hẳn đèn LED để bảo vệ linh kiện
    led.close()      # Giải phóng chân GPIO 25
    print("Đã dọn dẹp chân GPIO. Tạm biệt!")