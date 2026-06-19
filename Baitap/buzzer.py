from gpiozero import Buzzer
from time import sleep

# Khai báo chân GPIO 6
buzzer = Buzzer(5)

print("--- BẮT ĐẦU TEST BUZZER ---")

# 1. Test kêu liên tục trong 2 giây
print("Đang test: Kêu liên tục trong 2 giây...")
buzzer.on()
sleep(2)
buzzer.off()
sleep(1)

# 2. Test kêu nhịp (tít tít) 3 lần
print("Đang test: Kêu nhịp (tít tít)...")
for i in range(3):
    buzzer.on()
    sleep(0.3)
    buzzer.off()
    sleep(0.3)

# 3. Test tính năng beep của thư viện (tốt cho Passive Buzzer)
print("Đang test: Chế độ Beep...")
buzzer.beep(on_time=0.1, off_time=0.1, n=5)

print("--- HOÀN THÀNH ---")