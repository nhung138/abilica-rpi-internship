# HƯỚNG DẪN CÀI ĐẶT MÔI TRƯỜNG VÀ THƯ VIỆN CHẠY DHT11 TRÊN RASPBERRY PI

# BƯỚC 1: Cập nhật hệ thống và cài đặt các gói lõi (chỉ cần chạy 1 lần cho máy)
#sudo apt-get update
#sudo apt-get install gpiod libgpiod-dev python3-venv python3-full -y

# BƯỚC 2: Tạo môi trường ảo (chỉ cần chạy 1 lần cho mỗi dự án mới)
# Lệnh này sẽ tạo một thư mục tên là 'dht-env' tại thư mục bạn đang đứng
#python3 -m venv dht-env

# BƯỚC 3: Kích hoạt môi trường ảo 
# LƯU Ý QUAN TRỌNG: Phải chạy lệnh này mỗi khi khởi động lại máy hoặc mở Terminal mới!
# Dấu hiệu thành công: Đầu dòng lệnh xuất hiện chữ (dht-env)
#source dht-env/bin/activate

# BƯỚC 4: Cài đặt thư viện Adafruit DHT (chỉ cần chạy 1 lần sau khi tạo venv)
#pip install adafruit-circuitpython-dht

# BƯỚC 5: Chạy chương trình
#python dht11.py

# BƯỚC PHỤ: Thoát môi trường ảo
# Nếu làm xong và muốn quay lại terminal bình thường của hệ điều hành, gõ lệnh:
# deactivate

###HOAC source dht-env/bin/activate roi chay la duoc


#neu ma chuong trinh khong hien thi, thi doi chan gpio

import time
import board
import adafruit_dht

# Khởi tạo cảm biến DHT11. 
# Giả sử chân DATA của cảm biến đang cắm vào chân GPIO17 trên mạch Raspberry Pi
dht_device = adafruit_dht.DHT11(board.D17) 

print("Bắt đầu đọc dữ liệu DHT11 trên Raspberry Pi...")

while True:
    try:
        # Lấy dữ liệu
        nhiet_do = dht_device.temperature
        do_am = dht_device.humidity
        
        print("Độ ẩm: {} %  |  Nhiệt độ: {} *C".format(do_am, nhiet_do))

    except RuntimeError as error:
        # DHT11 khá nhạy cảm với việc đọc liên tục trên Linux, 
        # thỉnh thoảng sẽ bị rớt nhịp, ta chỉ cần in lỗi và thử lại
        print("Đang thử lại... ({})".format(error.args[0]))
        time.sleep(2.0)
        continue
    except Exception as error:
        # Dừng hẳn cảm biến nếu gặp lỗi hệ thống nghiêm trọng
        dht_device.exit()
        raise error

    # Đợi 2 giây trước khi đọc lần tiếp theo
    time.sleep(2.0)