from gpiozero import MotionSensor
from signal import pause
import time

class SmartMotionDetector:
    def __init__(self, pin, hold_time=5):
        # hold_time: Thời gian đèn vẫn sáng sau khi không còn chuyển động (giây)
        # queue_len=3: Lọc nhiễu cứng, chỉ báo nếu có tín hiệu liên tục
        self.pir = MotionSensor(pin, queue_len=3, sample_rate=10)
        self.pir.when_motion = self.motion_detected
        self.pir.when_no_motion = self.no_motion_detected
        self.hold_time = hold_time
        self.last_active = 0
        print(f"Hệ thống đã khởi động trên chân GPIO {pin}...")

    def motion_detected(self):
        self.last_active = time.time()
        print(f"[{time.strftime('%H:%M:%S')}] Chuyển động: BẬT ĐÈN")

    def no_motion_detected(self):
        # Kiểm tra nếu đã quá thời gian hold_time thì mới tắt
        print(f"[{time.strftime('%H:%M:%S')}] Không có người, chờ tắt...")

# Khởi tạo và chạy
if __name__ == "__main__":
    # Sử dụng chân 17, giữ trạng thái bật 5 giây sau khi hết chuyển động
    detector = SmartMotionDetector(pin=17, hold_time=5)
    try:
        pause()
    except KeyboardInterrupt:
        print("\nĐã dừng hệ thống.")